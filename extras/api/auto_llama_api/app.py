import os
from pathlib import Path
from argparse import ArgumentParser
from importlib.metadata import version

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auto_llama_api.models import Version
from auto_llama_api.routes import openaiRouter

BASE_PATH = Path(__file__).parent.absolute()
TITLE = "AutoLLama API"

app = FastAPI(title=TITLE, version=version("auto-llama-api"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(openaiRouter)


@app.get("/", response_model=Version, tags=["Welcome"])
async def root():
    """Base route with status message"""

    return Version(message="Welcome to the AutoLLaMa API!", version=app.version)


def main():
    """Start FastAPI Server"""

    parser = ArgumentParser(description=TITLE)
    parser.add_argument("-p", "--port", type=int, help="Port on which the API will listen", default=8000)
    parser.add_argument("-s", "--share", action="store_true", help="Allow API access from other devices")
    parser.add_argument("-r", "--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default=".env",
        help="Environment file to load (default: ./.env)",
    )

    args = parser.parse_args()

    if os.path.exists(args.env):
        load_dotenv(dotenv_path=args.env)

    uvicorn.run("auto_llama_api:app", host="0.0.0.0" if args.share else "127.0.0.1", port=args.port, reload=args.reload)
