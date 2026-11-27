"""Pydantic models for request and response validation."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    """Payload used to create an item."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(..., ge=0, description="Non-negative price")


class Item(ItemCreate):
    """An item as returned by the API."""

    id: int = Field(..., ge=1)
