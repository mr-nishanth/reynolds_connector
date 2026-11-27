"""Item endpoints under /api/v1/items."""

from fastapi import APIRouter, HTTPException, Path, status

from app import store
from app.schemas import Item, ItemCreate

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.get("", response_model=list[Item])
def list_items() -> list[Item]:
    """List all sample items."""
    return store.list_items()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int = Path(..., ge=1)) -> Item:
    """Get a single item by id. Returns 404 if the id is unknown."""
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    """Create a new item and return it with its assigned id."""
    return store.create_item(payload)
