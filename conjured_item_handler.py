from item import Item
from item_handler import ItemHandler
from item_names import AGED_BRIE, CONJURED_ITEM_PREFIX
from standard_item_handler import StandardItemHandler


class ConjuredItemHandler(StandardItemHandler):
    def can_handle(self, item: Item) -> bool:
        return item.name.casefold().startswith(CONJURED_ITEM_PREFIX)

    @property
    def quality_decay_factor(self) -> int:
        return 2 # "Conjured" items degrade in Quality twice as fast as normal items
