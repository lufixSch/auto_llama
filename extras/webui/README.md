# AutoLLama UI

SvelteKit based Chat UI for LLMs which works with any OpenAI compatible API

I plan on adding some features which will only work with AutoLLaMa but I will add it in a way, that the base functionality will still work with any OpenAI compatible API.

## Usage

Before starting the WebUI the first time, you need to add a `.env` file to this directory with the following variables:

```env
DATA_PATH="./data"
PUBLIC_OPEN_AI_ENDPOINT="http://localhost:5000/v1"
PUBLIC_OPEN_AI_KEY="sk-11111111111111111111111111"
```

`DATA_PATH` defines where the UI will store data like chats and other information.

> **⚠️ WARNING: The OpenAI API key will be exposed to everyone loading the webpage!**

You can run the WebUI with the following commands:

```
npm install
npm run build
npm run preview
```

> For a complete production build follow the instructions [here](https://kit.svelte.dev/docs/adapter-node)
