from item import Item
from item_handler import ItemHandler
from item_names import AGED_BRIE, SULFURAS
from standard_item_handler import StandardItemHandler


class SulfurasHandler(ItemHandler):
    def can_handle(self, item: Item) -> bool:
        return item.name == SULFURAS

    def update_quality(self, item: Item):
        pass # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
