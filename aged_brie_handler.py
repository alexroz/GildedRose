from item import Item
from item_handler import ItemHandler
from item_names import AGED_BRIE
from standard_item_handler import StandardItemHandler


class AgedBrieHandler(StandardItemHandler):
    def can_handle(self, item: Item) -> bool:
        return item.name == AGED_BRIE

    @property
    def quality_decay_factor(self) -> int:
        return -1 # "Aged Brie" actually increases in Quality the older it gets
