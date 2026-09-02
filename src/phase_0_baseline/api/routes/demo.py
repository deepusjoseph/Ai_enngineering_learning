import asyncio
import logging
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from phase_0_baseline.config import Settings
from phase_0_baseline.dependencies import get_settings
from phase_0_baseline.model import EchoRequest, EchoResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Phase 0 Baseline API is running"}


@router.post("/echo", response_model=EchoResponse)
async def echo(request: EchoRequest) -> EchoResponse:
    logger.info("Echo request received")
    return EchoResponse(
        message=request.message,
        length=len(request.message),
    )


async def generate_chunks() -> AsyncGenerator[str, None]:
    chunks = ["Hello", " ", "from", " ", "streaming", "!"]

    for chunk in chunks:
        logger.debug("Sending stream chunk")
        await asyncio.sleep(0.5)
        yield chunk


@router.get("/stream")
async def stream() -> StreamingResponse:
    return StreamingResponse(
        generate_chunks(),
        media_type="text/plain",
    )


@router.get("/config")
async def get_config(
    app_settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    return {
        "app_name": app_settings.app_name,
        "environment": app_settings.environment,
        "log_level": app_settings.log_level,
    }


@router.get("/items/{item_id}")
async def get_item(item_id: int) -> dict[str, int]:
    if item_id != 1:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return {
        "item_id": item_id,
    }
