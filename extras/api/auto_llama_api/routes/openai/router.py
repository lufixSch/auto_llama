from fastapi import APIRouter
from .completions import completionRouter

openaiRouter = APIRouter(prefix="/v1", tags=["OpenAI"])
openaiRouter.include_router(completionRouter)
