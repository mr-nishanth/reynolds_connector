"""Application entry point.

Run with: uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.items import router as items_router

app = FastAPI(
    title="Reynolds Connector API",
    version="0.1.0",
    description="Sample FastAPI service for the reynolds-connector repository.",
)

app.include_router(items_router)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Return a welcome message."""
    return {"message": "Welcome to the Reynolds Connector API"}


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "ok"}
