import unittest
from unittest import mock
from aged_brie_handler import AgedBrieHandler
from backstage_passes_handler import BackstagePassesHandler
from conjured_item_handler import ConjuredItemHandler
from item import Item
import item_updater
from standard_item_handler import StandardItemHandler
from sulfuras_handler import SulfurasHandler


class ItemUpdaterTest(unittest.TestCase):
    def test_configured_handlers(self):
        # Intent is to shout loudly if the configuration is changed
        # to avoid unintended modifications
        self.assertEqual(5, len(item_updater.ORDERED_HANDLERS))
        self.assertIsInstance(item_updater.ORDERED_HANDLERS[0], SulfurasHandler)
        self.assertIsInstance(item_updater.ORDERED_HANDLERS[1], BackstagePassesHandler)
        self.assertIsInstance(item_updater.ORDERED_HANDLERS[2], AgedBrieHandler)
        self.assertIsInstance(item_updater.ORDERED_HANDLERS[3], ConjuredItemHandler)
        self.assertIsInstance(item_updater.ORDERED_HANDLERS[4], StandardItemHandler)

    def test_no_handler_exception(self):
        mock_handlers = mock.patch.object(
            item_updater, "ORDERED_HANDLERS", return_value=[]
        )

        with mock_handlers:
            with self.assertRaises(NotImplementedError) as context:
                item_updater.update_item(
                    Item(name="my test item", sell_in=666, quality=777)
                )
                self.assertEqual(
                    str(context.exception), "No handler for item: my test item"
                )
