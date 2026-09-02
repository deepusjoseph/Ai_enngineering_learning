import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from phase_0_baseline.api.routes.demo import router as demo_router
from phase_0_baseline.api.routes.health import router as health_router
from phase_0_baseline.config import settings
from phase_0_baseline.logging_config import configure_logging
from phase_0_baseline.middleware import RequestLoggingMiddleware

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Application starting")

    yield

    logger.info("Application shutting down")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(health_router)
app.include_router(demo_router)
