"""In-memory item store.

Data is not persisted; it resets when the process restarts or when
``reset_store`` is called (used by tests).
"""

from typing import Optional

from app.schemas import Item, ItemCreate

_SEED_ITEMS = [
    {"name": "Sample Widget", "description": "A basic sample widget", "price": 9.99},
    {"name": "Sample Gadget", "description": None, "price": 24.5},
    {"name": "Sample Gizmo", "description": "A small gizmo", "price": 0.0},
]

_items: dict[int, Item] = {}
_next_id: int = 1


def reset_store() -> None:
    """Clear the store and re-seed it with the sample items."""
    global _next_id
    _items.clear()
    _next_id = 1
    for data in _SEED_ITEMS:
        create_item(ItemCreate(**data))


def list_items() -> list[Item]:
    """Return all items ordered by id."""
    return [_items[item_id] for item_id in sorted(_items)]


def get_item(item_id: int) -> Optional[Item]:
    """Return the item with the given id, or None if it does not exist."""
    return _items.get(item_id)


def create_item(payload: ItemCreate) -> Item:
    """Store a new item and return it with its assigned id."""
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _items[item.id] = item
    _next_id += 1
    return item


reset_store()
