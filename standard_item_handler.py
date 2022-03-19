from item import Item
from item_handler import ItemHandler


class StandardItemHandler(ItemHandler):
    def can_handle(self, item: Item) -> bool:
        return True

    def update_quality(self, item: Item):
        item.sell_in -= 1
        quality_diff = self.quality_decay_factor * (-1 if item.sell_in >= 0 else -2)
        # clamp quality between 0 and 50
        item.quality = min(50, max(0, item.quality + quality_diff))
