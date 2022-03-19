from item import Item
from item_handler import ItemHandler
from item_names import AGED_BRIE, BACKSTAGE_PASSES
from standard_item_handler import StandardItemHandler


class BackstagePassesHandler(ItemHandler):
    def can_handle(self, item: Item) -> bool:
        return item.name == BACKSTAGE_PASSES

    def update_quality(self, item: Item):
        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = 0
            return

        if item.sell_in > 9:
            quality_diff = 1
        elif item.sell_in > 4:
            quality_diff = 2
        else:
            quality_diff = 3

        # standard quality max 50 still applies
        item.quality = min(50, item.quality + quality_diff)
