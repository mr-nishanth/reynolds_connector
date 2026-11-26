"""Typed API schemas published to dependent repositories."""

from pydantic import BaseModel, ConfigDict


class VehicleRecord(BaseModel):
    """A vehicle returned by GET /vehicles/{vin}."""

    model_config = ConfigDict(frozen=True)

    vin: str
    make: str
    model: str
    year: int


class ErrorResponse(BaseModel):
    """Error body returned for 404 responses."""

    detail: str
