from typing import Literal

from auto_llama import exceptions, ChatToObjectiveConverter, Chat, ModelLoader

from string import punctuation

HAS_DEPENDENCIES = True

try:
    import spacy
    from spacy.tokens import Token
    from spacy.language import Language
    import coreferee
    from coreferee.data_model import ChainHolder
except ImportError:
    #    raise exceptions.ExtrasDependenciesMissing("nlp", "nlp")
    HAS_DEPENDENCIES = False


def _load_spacy():
    try:
        nlp = spacy.load("en_core_web_trf")
        nlp.add_pipe("coreferee")
    except coreferee.errors.VectorsModelNotInstalledError:
        raise exceptions.ModelMissing("spacy")
    except OSError:
        raise exceptions.ModelMissing("spacy")


if HAS_DEPENDENCIES:
    ModelLoader.add("spacy", _load_spacy)


class CorefResChatConverter(ChatToObjectiveConverter):
    """Extract objective from chat history using the last message and coreference resolution to improve context"""

    def __init__(self, msg_cnt: int | Literal["all"] = 3) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.PreprocessorDependenciesMissing(self.__class__.__name__, "coref")

        self._msg_cnt = msg_cnt

    def __call__(self, chat: Chat) -> str:
        nlp = ModelLoader.get("spacy", Language)

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
