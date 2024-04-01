"""OpenAI API completion routes"""

import asyncio
from fastapi import APIRouter
from fastapi.requests import Request
from sse_starlette import EventSourceResponse
from uuid import uuid4
from datetime import datetime, UTC

from auto_llama_api.models import (
    OpenAICompletion,
    OpenAICompletionResponseBase,
    OpenAICompletionResponse,
    OpenAICompletionChoice,
    OpenAIChatCompletion,
    OpenAIChatCompletionResponse,
    OpenAIChatChoice,
    OpenAIChatStreamChoice,
    OpenAIMessage,
)
from auto_llama_api.lib import LLMInterface

from auto_llama import Chat

completionRouter = APIRouter()

streaming_semaphore = asyncio.Semaphore(1)


@completionRouter.post("/completions", response_model=OpenAICompletionResponse)
def openai_completion(req: Request, args: OpenAICompletion, llm: LLMInterface):
    res_id = f"cmpl-{uuid4().hex}"
    stop = args.stop if isinstance(args.stop, list) else [args.stop]
    cmpl_response = OpenAICompletionResponse(
        id=res_id,
        object="text_completion",
        model=args.model,
        created=round(datetime.now(UTC).timestamp()),
        system_fingerprint="none",
        usage=OpenAICompletionResponseBase.Usage(completion_tokens=0, prompt_tokens=0, total_tokens=0),
        choices=[],
    )

    if not args.stream:
        response = llm.completion(args.prompt, stopping_strings=stop, max_new_tokens=args.max_tokens)
        cmpl_response.choices.append(OpenAICompletionChoice(finish_reason="length", index=0, text=response))
        return cmpl_response

    stream = llm.completion_stream(args.prompt, stopping_strings=stop, max_new_tokens=args.max_tokens)

    async def create_stream_response(stream):
        async with streaming_semaphore:
            for el in stream:
                if await req.is_disconnected():
                    break

                cmpl_response.choices = [OpenAICompletionChoice(index=0, text=el)]
                yield {"data": cmpl_response.model_dump_json()}

    return EventSourceResponse(create_stream_response(stream))


@completionRouter.post("/chat/completions", response_model=OpenAIChatCompletionResponse)
def openai_chat_completion(req: Request, args: OpenAIChatCompletion, llm: LLMInterface):
    res_id = f"chatcmpl-{uuid4().hex}"
    stop = args.stop if isinstance(args.stop, list) else [args.stop]
    cmpl_response = OpenAIChatCompletionResponse(
        id=res_id, object="chat.completion", created=round(datetime.now(UTC).timestamp()), choices=[]
    )

    chat = Chat.from_history(history=[msg.to_chat() for msg in args.messages])

    if not args.stream:
        response = llm.chat(chat, stopping_strings=stop, max_new_tokens=args.max_tokens).last
        cmpl_response.choices.append(
            OpenAIChatChoice(
                index=0,
                message=OpenAIChatChoice.Message(role=OpenAIMessage.Role(response.role), content=response.message),
            )
        )
        return cmpl_response

    stream = llm.chat_stream(chat, stopping_strings=stop, max_new_tokens=args.max_tokens)

    async def create_stream_response(stream):
        async with streaming_semaphore:
            for el in stream:
                if await req.is_disconnected():
                    break

                cmpl_response.choices = [
                    (
                        OpenAIChatStreamChoice(
                            index=0, delta=OpenAIChatStreamChoice.Message(content=el, role=OpenAIMessage.Role.ASSISTANT)
                        )
                    )
                ]
                yield {"data": cmpl_response.model_dump_json()}

    return EventSourceResponse(create_stream_response(stream))
