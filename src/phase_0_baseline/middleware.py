import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        logger.info(
            "Request started | method=%s | path=%s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "Request completed | method=%s | path=%s | status=%s | duration=%.4fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response