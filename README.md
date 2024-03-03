# AutoLLaMa

Supercharge your local LLM with AutoLLaMa!

This project is a union off different concepts/ideas to improve the capabilities of LLMs. It is build to be a library, that can be used to get started with any LLM related project.

> **ℹ️ NOTE:** Maybe you also found my text_generation_webui_auto_llama repository on GitHub. This is **NOT** an extension of auto-llama for oobabooga/text-generation-webui!

> **⚠️ WARNING: This project is still in early development! Things (like restructuring the whole project) may change without any notice!**

## Introduction

AutoLLaMa itself is just a set classes to ensure interoperability between different libraries and projects. Additionally this repository contains some baseimplementation of often needed tools, like RAG (`auto_llama_memory`) and function calling (`auto_llama_agents`)

The following packages are part of this repository:

- `auto_llama`: The core of the project. It provides classes to implement an LLM, a generic Chat class and some more
  - `text`: Text processing tools
  - `audio`: Audio processing tools
- `auto_llama_agents`: A function calling system, with solutions for deciding which Agent to call depending on the conversation
- `auto_llama_memory`: A long term memory solution for generic data and conversations

Every package is designed to be used independently of all other packages (except `auto_llama`).

## Install

At the moment it is not possible to install AutoLLaMa using `pip`. You can either install the prebuild wheels from GitHub or install it directly from source.

In order to make the package light weight there are optional dependencies defined separately for each package/submodule. You cann install them separately.

_Example:_

```bash
pip install auto-llama[agents.code]
pip install auto-llama[extras.text]
```

### Prebuild wheel

There are prebuild wheels of this package available on the GitHub [releases](https://github.com/LufixSch/AutoLLaMa/releases). They can be installed as follows:

```bash
pip install auto-llama --index-url https://github.com/lufixSch/auto_llama/releases/download/latest/
```

> If you just want a specific version replace `latest` with the version you are interested in.

### From source

1. Clone the repository
2. `pip install .` in the root directory of the repository

In order to make the package light weight there are optional dependencies defined separately for each package. You cann install them separately.

### Development

Install the package in editable mode

```bash
pip install -e .[<optional_dependencies>]
```

## Ideas

Here are some ideas for additional features, that I'm working on or plan to work on:

- [ ] Improve logging interface
  - [ ] Add logging base class
  - [ ] Allow submodules to log as the Agent from which they where called
- [ ] Improve Memory
  - [ ] Fetch more information than necessary and filter with _similarity_ to improve accuracy
  - [x] Optionally pass source(s) on `Memory.save`
  - [ ] Save original (unprocessed) data _Optional_
  - [ ] Retrieve window of data around the matching segment
  - [ ] add sliding window paragraphing instead of splitting
- [ ] Text loader
  - [ ] ImageTextLoader -> Get text from image
  - [ ] PdfTextLoader -> Get text from PDF (maybe try to get equations in some way)
- [ ] More Agents
- [ ] Improve Chat class
  - [ ] Multi user chat
  - [ ] Improve Chat memory interface
    - [ ] Load/Save chat from/to database (possibly Embeddings DB)
- [ ] Rework selectors to allow multiple agents to be used
  - [ ] Multi Agent selector
  - [ ] Generate multiple objectives from one input
  - [ ] Run multiple agents with their corresponding objective
- [ ] Add trigger (e.g. interface for external sources to trigger an LLM response or agent)
- [ ] Rework with multithreading
- [ ] Add time aware memory (No Idea how to do this!)
  - [ ] Idea: _Fetch x recent memory's and y memory's (time independent) and mark them as recent/general_
  - [x] add time tracking to chat messages
- [ ] Add custom prompt templates
- [ ] Add image/multimodal memory (Supported by txtai out of the box)
- [ ] Speach
  - [x] Add TTS
    - [ ] Realtime/Stream TTS
    - [ ] cuqoi-ai TTS
    - [ ] vocoder or similar
    - [ ] voice clone
  - [x] Add transcription (realtime transscript)
    - [ ] Realtime/Stream Transscript

## Contributing

You can contribute to the project by submitting a pull request or by opening an issue for bugs or feature requests. I'm always open for new ideas 😃
