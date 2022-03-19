from typing import List
from aged_brie_handler import AgedBrieHandler
from backstage_passes_handler import BackstagePassesHandler
from item import Item
from item_handler import ItemHandler
from standard_item_handler import StandardItemHandler
from sulfuras_handler import SulfurasHandler

# Hardcoded here for simplicity
# For a variety of reasons, we'd normally have these handlers registered/configured
# elsewhere
ORDERED_HANDLERS: List[ItemHandler] = [
    SulfurasHandler(),
    BackstagePassesHandler(),
    AgedBrieHandler(),
    # default, could also be the hardcoded fallback in update_item
    StandardItemHandler(),
]


def update_item(item: Item) -> None:
    for handler in ORDERED_HANDLERS:
        if handler.can_handle(item):
            handler.update_quality(item)
            return

    raise NotImplementedError(f"No handler for item: {item.name}")
