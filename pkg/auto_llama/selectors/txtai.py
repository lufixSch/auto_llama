"""txtai based manager"""

from auto_llama import AgentSelector, Agent, ModelLoader
from auto_llama.exceptions import ModuleDependenciesMissing

try:
    from txtai.pipeline import Similarity
except ImportError:
    raise ModuleDependenciesMissing("nlp", "nlp")

ModelLoader.add("txtai.similarity", lambda: Similarity())


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

        self._tools = tools
        self._keyword_mapping = KeywordMapping(assistant=none_keywords, **keywords)

    def _run(self, prompt: str) -> Agent:
        similarities = ModelLoader.get("txtai.similarity", Similarity)(prompt, self._keyword_mapping.keywords_flat)

        keyword = self._keyword_mapping.keywords_flat[similarities[0][0]]
        tool = self._keyword_mapping.name(keyword)

        if tool == "assistant":
            return None

        return self._tools[tool]
