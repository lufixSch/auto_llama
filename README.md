# AutoLLaMa

Supercharge your local LLM with different agents

This project is a union off different smaller ideas I had/build to improve the capabilities of LLMs, build into a modular framework. The framework is built to be extendable, so feel free to experiment with it.

> **ℹ️ NOTE:** Maybe you also found my text_generation_webui_auto_llama repository on GitHub. This is **NOT** (yet) a extension of auto-llama for oobabooga/text-generation-webui!

> **⚠️ WARNING: This project is still in early development!**

## Framework

At the moment the framework is based on four main ideas:

1. Agents - Agent that uses an LLM and/or other tools to perform a specific task derived from a single prompt or a chat history.
2. Managers - A system that decides which agent to use for a given prompt or chat history. However, the boundaries between Agents and Managers are not clear cut (see for example `auto_llama.agents.research.ResearchAgent`)
3. Memory - A system that stores information across agents and prompts to improve the performance of the system.
4. LLMs - A interface to interact with a LLM for regular text generation and chat.

Additionally the `auto_llama` module provides some submodules with helpful utilities.

1. nlp - Some functions for text processing
2. react - Small ReAct framework to make an implementation easier

## Implementations

### Agents

There are a few agents implemented currently. They are accessible over the `auto_llama.agents` module:

- code - Agents based around executing code in a sandbox environment (Docker container)
  - CodeExecAgent - Executes code included in the prompt or last chat message
  - CodeAgent - Uses an LLM to generate code based on a objective and executes it
- research - Agents based around finding information in the internet
  - SearchAgent: Retrieves information using a single tool (e.g. WikipediaSearchAgent, DuckDuckGoSearchAgent)
  - ResearchAgent: Thoroughly researchs a given topic using multiple SearchAgents and ReAct

There are also some implementeds of text input or chat preprocessors available:

- TemplateInputPreprocessor - Extract an objective from a prompt using _begin_ and _end_ keywords.
- nlp - Improved preprocessing using nlp
  - CorefResChatPreprocessor - Extract objective from chat history using the last message and coreference resolution to improve context

## Installation

At the moment it is not possible to install AutoLLaMa using `pip`. You need to install it from source.

1. Clone the repository
2. `pip install .` in the root directory of the repository

In order to make the package light weight there are optional dependencies defined separately for each submodule or group of agents. You cann install them separately.

_Example:_

```bash
pip install .[agent.code]
pip install .[module.nlp]
```

To install all dependencies, run `pip install .[all]`. This will install all optional dependencies for the project.

> **ℹ️ NOTE:** Optional dependencies including the `nlp` module (e.g. `module.nlp`, `agent.research` ...) will install torch. Depending on you system you might want to install it beforehand.

> **ℹ️ NOTE:** Modules using the `nlp` optional dependency group (e.g. `module.nlp`, `agent.research`, `agent.preprocessor.nlp`) might need you to download _spaCy_ or _nltk_ models. Use `bin/nltk_ressources.py` and `bin/spacy_ressources.py` for easy installation of necessary ressources.

### Development

Install the package in editable mode

```bash
pip install -e .[<opional_dependencies>]
```

## ToDo

- Add Manager implementations
  - CommandManager - Select agent based on a command (e.g. /code, /search ...)
  - KeywordManager - Select agent based on keywords in the input
  - AutoManager - Automatically decides which agent to use based on the context
- Improve agent response system
  - Rework response types -> don't force a position, just give information about the response
- Improve agent `run_chat` default
- Add time aware memory (No Idea how to do this!)
  - Idea: _Fetch x recent memory's and y memory's (time independent) and mark them as recent/general_
- Add image/multimodal memory (Supported by txtai out of the box)
