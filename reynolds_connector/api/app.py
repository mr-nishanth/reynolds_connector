"""FastAPI application for the Reynolds connector backend."""

from fastapi import FastAPI

from reynolds_connector.api.vehicles import router as vehicles_router

app = FastAPI(title="Reynolds Connector API")
app.include_router(vehicles_router)
