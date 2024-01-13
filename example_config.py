from auto_llama_cli import CLIConfig
from auto_llama.llm import LocalOpenAILLM
from auto_llama.agents import MultiSearchAgent, WikipediaSearchAgent, DuckDuckGoSearchAgent
from auto_llama.preprocessors import CorefResChatConverter
from auto_llama.selectors import SimilarityAgentSelector
from auto_llama.memory import TxtAIConversationMemory, TxtAIMemory

# LLM -----------------------------------------------------
llm = LocalOpenAILLM(base_url="http://localhost:5000/v1")

# Memory -----------------------------------------------------
facts_memory = TxtAIMemory()
conversation_memory = TxtAIConversationMemory()

# Agents -----------------------------------------------------
search_agent = MultiSearchAgent(
    [DuckDuckGoSearchAgent(facts_memory, max_results=3), WikipediaSearchAgent(facts_memory, 2)]
)
agents = {"search", search_agent}

# Selector -----------------------------------------------------
agent_keywords = {
    "search": ["research knowledge in a encyclopedia", "search the web using a search engine"],
}
assistant_keywords = ["talk to a friend", "talk to a assistant", "answer personal questions"]
selector = SimilarityAgentSelector(agents, agent_keywords, assistant_keywords)

# Preprocessor -----------------------------------------------------
chat_converter = CorefResChatConverter()

config = CLIConfig(llm, agents, selector, chat_converter, facts_memory, conversation_memory)
