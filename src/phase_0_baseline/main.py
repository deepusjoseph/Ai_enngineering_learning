import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from phase_0_baseline.model import EchoRequest, EchoResponse

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Phase 0 Baseline API is running"}


@app.post("/echo", response_model=EchoResponse)
async def echo(request: EchoRequest) -> EchoResponse:
    return EchoResponse(
        message=request.message,
        length=len(request.message),
    )


async def generate_chunks():
    chunks = ["Hello", " ", "from", " ", "streaming", "!"]

    for chunk in chunks:
        await asyncio.sleep(0.5)
        yield chunk


@app.get("/stream")
async def stream() -> StreamingResponse:
    return StreamingResponse(
        generate_chunks(),
        media_type="text/plain",
    )
