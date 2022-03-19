# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from itertools import zip_longest
from typing import List
from item import Item

from item_names import AGED_BRIE, BACKSTAGE_PASSES, CONJURED_ITEM_EXAMPLE, STANDARD_ITEM, SULFURAS

class GildedRoseTest(unittest.TestCase):

    # test evidence based on provided texttest fixture
    # todo: remove when no longer required
    def test_legacy(self):
        items: List[Item] = [
             Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
             Item(name="Aged Brie", sell_in=2, quality=0),
             Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
             # Removing as original implementation did not handle conjured items
             # Leaving here only as a note for the exercise
             # Item(name="Conjured Mana Cake", sell_in=3, quality=6),
            ]
        
        expected_day_one: List[Item] = [
             Item(name="+5 Dexterity Vest", sell_in=9, quality=19),
             Item(name="Aged Brie", sell_in=1, quality=1),
             Item(name="Elixir of the Mongoose", sell_in=4, quality=6),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=14, quality=21),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=50),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=4, quality=50),
             # Item(name="Conjured Mana Cake", sell_in=2, quality=5),
        ]

        expected_day_two: List[Item] = [
             Item(name="+5 Dexterity Vest", sell_in=8, quality=18),
             Item(name="Aged Brie", sell_in=0, quality=2),
             Item(name="Elixir of the Mongoose", sell_in=3, quality=5),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
             Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=13, quality=22),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=8, quality=50),
             Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=50),
             # Item(name="Conjured Mana Cake", sell_in=1, quality=4),
        ]

        GildedRose(items).update_quality()
        self._validate_items(items, expected_day_one)

        GildedRose(items).update_quality()
        self._validate_items(items, expected_day_two)

    def test_update_decreases_sellin_and_quality(self):
        item = Item(name=STANDARD_ITEM, sell_in=10, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=STANDARD_ITEM, sell_in=9, quality=19))

    def test_update_quality_does_not_go_below_zero(self):
        item = Item(name=STANDARD_ITEM, sell_in=10, quality=0)
        result = self._act(item)
        self._validate(result, Item(name=STANDARD_ITEM, sell_in=9, quality=0))

    def test_update_quality_goes_down_two_after_use_by(self):
        item = Item(name=STANDARD_ITEM, sell_in=0, quality=10)
        result = self._act(item)
        self._validate(result, Item(name=STANDARD_ITEM, sell_in=-1, quality=8))

    def test_update_aged_brie_increases_in_quality(self):
        item = Item(name=AGED_BRIE, sell_in=10, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=AGED_BRIE, sell_in=9, quality=21))

    def test_update_aged_brie_quality_increases_by_two_quality_after_sell_by(self):
        item = Item(name=AGED_BRIE, sell_in=0, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=AGED_BRIE, sell_in=-1, quality=22))

    def test_update_aged_brie_does_not_increase_above_fifty(self):
        item = Item(name=AGED_BRIE, sell_in=10, quality=50)
        result = self._act(item)
        self._validate(result, Item(name=AGED_BRIE, sell_in=9, quality=50))

    def test_update_sulfuras_does_not_change_values(self):
        item = Item(name=SULFURAS, sell_in=666, quality=777)
        result = self._act(item)
        self._validate(result, Item(name=SULFURAS, sell_in=666, quality=777)) 

    def test_update_sulfuras_does_not_change_values(self):
        item = Item(name=SULFURAS, sell_in=666, quality=777)
        result = self._act(item)
        self._validate(result, Item(name=SULFURAS, sell_in=666, quality=777))

    def test_update_backstage_passes_increases_quality(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=11, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=10, quality=21)) 

    def test_update_backstage_passes_increases_quality_by_two_when_10_days_remain(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=10, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=9, quality=22))

    def test_update_backstage_passes_increases_quality_by_two_when_less_than_10_days_remain(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=6, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=5, quality=22))

    def test_update_backstage_passes_increases_quality_by_three_when_5_days_remain(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=5, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=4, quality=23)) 

    def test_update_backstage_passes_increases_quality_by_three_when_less_than_5_days_remain(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=1, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=0, quality=23)) 

    def test_update_backstage_passes_quality_is_zero_after_event(self):
        item = Item(name=BACKSTAGE_PASSES, sell_in=0, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=BACKSTAGE_PASSES, sell_in=-1, quality=0)) 

    def test_update_conjured_item_decreases_by_two(self):
        item = Item(name=CONJURED_ITEM_EXAMPLE, sell_in=10, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=CONJURED_ITEM_EXAMPLE, sell_in=9, quality=18))

    def test_update_conjured_item_past_sell_by_decreases_by_four(self):
        item = Item(name=CONJURED_ITEM_EXAMPLE, sell_in=0, quality=20)
        result = self._act(item)
        self._validate(result, Item(name=CONJURED_ITEM_EXAMPLE, sell_in=-1, quality=16))

    def _act(self, item: Item) -> Item:
        items = [item]
        GildedRose(items).update_quality()
        return items[0]

    def _validate_items(self, items: List[Item], expected_items: List[Item]):
        for item, expected in zip_longest(items, expected_items):
            self._validate(item, expected)

    def _validate(self, item: Item, expected: Item):
        self.assertEqual(item.name, expected.name)
        self.assertEqual(item.sell_in, expected.sell_in)
        self.assertEqual(item.quality, expected.quality)
         
if __name__ == '__main__':
    unittest.main()
