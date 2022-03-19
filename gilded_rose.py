# -*- coding: utf-8 -*-

from item_updater import update_item


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            update_item(item)
