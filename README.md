# AutoLLaMa

Supercharge your local LLM with different agents

This project is a union off different smaller ideas I had/build to improve the capabilities of LLMs, build into a modular framework. The framework is built to be extendable, so feel free to experiment with it.

> **ℹ️ NOTE:** Maybe you also found my text_generation_webui_auto_llama repository on GitHub. This is **NOT** (yet) a extension of auto-llama for oobabooga/text-generation-webui!

> **⚠️ WARNING: This project is still in early development!**

## Framework

The framework is based on the following main ideas:

1. Agents - Agent that uses an LLM and/or other tools to perform a specific task derived from a single prompt or a chat history.
2. Selectors - A system that decides which agent to use for a given prompt or chat history.
3. Memory - A system that stores information across agents and prompts to improve the performance of the system.
4. LLMs - A interface to interact with a LLM for regular text generation and chat.
5. Assistant - A class that combines the above to provide an easy to use but configurable chat bot interface

This ideas can be expanded for more complex use cases with the following Tools:

1. Speech - Tools/Interfaces for Speech recognition/TTS

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

### Selectors

The selectors are accessible over the `auto_llama.selectors` module:

- CommandAgentSelector - Decides which Agent to use by checking for a command at the start of the prompt
- KeywordAgentSelector - Decides which Agent to use by checking for keywords in the prompt
- txtai - Manager using the txtai framework
  - SimilarityAgentManager - Classifies prompt using keywords for each tool. The results determine which tool is used

### Preprocessors

There are also some implementations of text input or chat preprocessors available (`auto_llama.preprocessors`):

- TemplateInputPreprocessor - Extract an objective from a prompt using _begin_ and _end_ keywords.
- nlp - Improved preprocessing using nlp
  - CorefResChatPreprocessor - Extract objective from chat history using the last message and coreference resolution to improve context

### Memory

Memory implementations are available in `auto_llama.memory`

- TxtAIMemory - Embeddings database for text or chat using the python `txtai` package

### Other

- speech - Tools/Interfaces for Speech recognition/TTS
  - txtai - Speech recognition and TTS using the txtai pipelines

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

- [ ] Add time aware memory (No Idea how to do this!)
  - [ ] Idea: _Fetch x recent memory's and y memory's (time independent) and mark them as recent/general_
  - [x] add time tracking to chat messages
- [ ] Add image/multimodal memory (Supported by txtai out of the box)
- [ ] Improve Chat class
  - [ ] Multi user chat
  - [ ] Improve Chat memory interface
    - [ ] Load/Save chat from/to database (possibly Embeddings DB)
- [ ] Improve logging interface
  - [ ] Add logging base class
  - [ ] Allow submodules to log as the Agent from which they where called
- [ ] Improve Memory
  - [ ] Fetch more information than necessary and filter with _similarity_ to improve accuracy
  - [x] Optionally pass source(s) on `Memory.save`
  - [ ] Save original (unprocessed) data
  - [ ] Retrieve window of data around the matching segment
  - [ ] add sliding window paragraphing instead of splitting
- [ ] Add custom prompt templates
- [ ] Rework selectors to allow multiple agents to be used
- [ ] Add trigger (e.g. interface for external sources to trigger an LLM response or agent)
- [ ] Rework with multithreading
- [ ] Speach
  - [x] Add TTS
    - [ ] Realtime/Stream TTS
    - [ ] cuqoi-ai TTS
    - [ ] vocoder or similar
    - [ ] voice clone
  - [x] Add transcription (realtime transscript)
    - [ ] Realtime/Stream Transscript
