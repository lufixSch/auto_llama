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

You then install the WebUI with the following commands:

```bash
npm install
npm run webui-install
```

Next you can run the WebUI with:

```bash
npm run webui
```

You can access the app at [localhost:3000](http://127.0.0.1:3000)

### Docker

This project also provides a docker container to run the WebUI. You can build and run it with the following commands:

```bash
docker build -t auto-llama-webui .
docker run --publish 3000:3000 --volume <data-directory>:/app/data
```

> `<data-directory>` should be the absolute path to the folder where you want your chats and characters to be saved.

If you want to run the container in the background add `--detatch` to the `docker run` command.
