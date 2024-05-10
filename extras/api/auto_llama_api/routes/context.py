from pathlib import Path
from uuid import uuid4

from auto_llama_api import settings
from auto_llama_api.lib import FileLoaders, UploadedFile
from auto_llama_api.models import FileInfo, FileLoadOptions
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from auto_llama.text import Summarizer

contextRouter = APIRouter(prefix="/context", tags=["AutoLLaMa"])


def json_form_checker(data: str = Form(...)):
    """Custom form loader for JSON data"""

    try:
        return FileLoadOptions.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@contextRouter.post("/", response_model=FileInfo)
async def upload_file(
    file: UploadedFile,
    loaders: FileLoaders,
    options: FileLoadOptions = Depends(json_form_checker),
):
    print(file)
    print(options)

    content = None
    for loader in loaders:
        if loader.is_valid(file):
            content = loader(file)
            break

    if not content:
        raise HTTPException(status_code=400, detail="Invalid file format")

    if options.ocr:
        raise HTTPException(status_code=400, detail="OCR not supported")

    if options.skip_appendix:
        lw_text = content.text.lower()
        ref_idx = lw_text.find("references\n")
        ap_idx = lw_text.find("appendix\n")

        if ref_idx != -1 and ap_idx != -1:
            content.text = content.text[: min(ref_idx, ap_idx)]

    if options.summarize:
        summarizer = Summarizer(content.text)
        max_len = int((1 - options.summarize) * summarizer.len())
        summary = summarizer.summarize(max_len)
        content.text = summary

    file_id = uuid4().hex
    path = Path(settings.DATA_PATH) / f"{file_id}.json"
    content.save(path)

    return FileInfo(id=file_id, title=content.title)
