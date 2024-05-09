from auto_llama_api.lib import ActiveMemory, ActiveMemorySetter, Memories
from auto_llama_api.models import ListResponse
from fastapi import APIRouter, HTTPException

memoryRouter = APIRouter(prefix="/memory", tags=["AutoLLaMa"])


@memoryRouter.get("/", response_model=ListResponse)
async def list_memory(memory: Memories):
    return ListResponse(items=list(memory.keys()))


@memoryRouter.post("/")
async def set_memory(memory_name: str | None, set_memory: ActiveMemorySetter, memory: Memories):
    if (memory is not None) and (memory_name not in memory.keys()):
        raise HTTPException(status_code=404, detail=f"Memory with name '{memory_name}' not found!")

    set_memory(memory_name)


@memoryRouter.post("/find")
async def search_memory(
    query: str,
    memory: ActiveMemory,
    memories: Memories,
    memory_name: str | None = None,
    max_tokens: int = 500,
    max_items: int = 10,
):
    if memory_name:
        memory = memories.get(memory_name, None)

        if not memory:
            raise HTTPException(status_code=404, detail=f"Memory with name '{memory_name}' not found!")

    if memory is None:
        raise HTTPException(status_code=404, detail="No memory activated!")

    res = memory.remember(query, max_tokens, max_items)

    return [e.serialize() for e in res]
