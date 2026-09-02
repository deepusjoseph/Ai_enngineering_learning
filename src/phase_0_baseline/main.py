import asyncio
import logging
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from phase_0_baseline.config import settings
from phase_0_baseline.logging_config import configure_logging
from phase_0_baseline.model import EchoRequest, EchoResponse

configure_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncIterator[None]:
    logger.info("Application starting")

    yield

    logger.info("Application shutting down")

app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Phase 0 Baseline API is running"}


@app.post("/echo", response_model=EchoResponse)
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


@app.get("/stream")
async def stream() -> StreamingResponse:
    return StreamingResponse(
        generate_chunks(),
        media_type="text/plain",
    )


@app.get("/config")
async def get_config() -> dict[str, str]:
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "log_level": settings.log_level,
    }
