"""txtai based selector"""

from string import punctuation
from typing import Literal

from auto_llama_agents import Agent, AgentResponse, AgentSelector

from auto_llama import Chat, ModelLoader, exceptions

HAS_DEPENDENCIES = True

try:
    import coreferee
    import spacy
    from coreferee.data_model import ChainHolder
    from spacy.language import Language
    from spacy.tokens import Token
    from txtai.pipeline import Similarity
except ImportError:
    HAS_DEPENDENCIES = False


def _load_spacy():
    try:
        nlp = spacy.load("en_core_web_trf")
        nlp.add_pipe("coreferee")

        return nlp
    except coreferee.errors.VectorsModelNotInstalledError:
        raise exceptions.ModelMissing("spacy")
    except OSError:
        raise exceptions.ModelMissing("spacy")


if HAS_DEPENDENCIES:
    ModelLoader.add("txtai.similarity", lambda: Similarity(path="BAAI/bge-reranker-base"))
    ModelLoader.add("coreferee", _load_spacy)


class KeywordMapping:
    """Bidirectional one-to-many, many-to-one mapping"""

    def __init__(self, assistant: list[str], **keywords: list[str]) -> None:
        self._keywords = keywords
        self._keywords["assistant"] = assistant

    @property
    def names(self):
        """List of all names"""

        self._keywords.keys()

    @property
    def keywords_flat(self):
        """Returns a flat array of all keywords"""

        values: list[str] = []
        for words in self._keywords.values():
            values.extend(words)

        return values

    def keywords(self, name: str):
        """Get the keywords matching a specific name"""

        return self._keywords[name]

    def name(self, keyword: str):
        """Find name matching this keyword"""

        for name, words in self._keywords.items():
            if keyword in words:
                return name

        raise ValueError(f"No matching name found for keyword: {keyword}")


class CorefResChatConverter:
    """Extract objective from chat history using the last message and coreference resolution to improve context"""

    def __init__(self, msg_cnt: int | Literal["all"] = 3) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.PreprocessorDependenciesMissing(self.__class__.__name__, "coref")

        self._msg_cnt = msg_cnt

    def __call__(self, chat: Chat) -> str:
        nlp = ModelLoader.get("coreferee", Language)

        if self._msg_cnt != "all":
            chat = chat.clone(-self._msg_cnt)

        conversation = (el.message for el in chat.history)

        # Ensure punctuation at the end of a message to improve accuracy
        conversation = list((el if el.rstrip()[-1] in punctuation else f"{el}." for el in conversation))

        doc = nlp(" ".join(conversation))
        last_msg = nlp(conversation[-1])

        offset = len(doc) - len(last_msg)
        maps: dict[str, str] = {}

        for i, token in enumerate(last_msg):
            conv_token = doc[offset + i]

            if token.pos_ == "PRON":
                coref: ChainHolder = conv_token._.coref_chains

                if coref:
                    for chain in coref:
                        for ref in chain:
                            ref_token: Token = doc[ref.root_index]

                            if ref_token.pos_ == "PROPN":
                                maps[token.text] = ref_token.text
                                break
                        else:
                            continue

                        break

        last_msg_str = conversation[-1]

        for original, resolved in maps.items():
            last_msg_str = last_msg_str.replace(original, resolved)

        return last_msg_str


class SimilarityAgentSelector(AgentSelector):
    """Automatically detect which agent is needed using similarity models"""

    def __init__(
        self,
        tools: dict[str, Agent],
        keywords: dict[str, list[str]],
        none_keywords: list[str] = ["communication", "assistant"],
    ):
        """
        Args:
            tools (dict[str, Agent]): Dictionary of available tools with their name as key
            keywords (dict[str, list[str]]): Keywords for each tool with the tool name as key.
            none_keywords (list[str]): Keywords which will map to no tool (e.g. no tool should be used)
        """

        if not HAS_DEPENDENCIES:
            raise exceptions.SelectorDependenciesMissing(self.__class__.__name__, "txtai")

        self._tools = tools
        self._keyword_mapping = KeywordMapping(assistant=none_keywords, **keywords)
        # self._coref_converter = CorefResChatConverter()  # TODO Add msg_cnt as configurable parameter

    def run(self, chat: Chat) -> AgentResponse:
        # prompt = self._coref_converter(chat)
        prompt = chat.last_from("user")
        similarities = ModelLoader.get("txtai.similarity", Similarity)(prompt, self._keyword_mapping.keywords_flat)

        keyword = self._keyword_mapping.keywords_flat[similarities[0][0]]
        tool = self._keyword_mapping.name(keyword)

        if tool == "assistant":
            return AgentResponse.empty()

        return self._tools[tool].run(prompt)
