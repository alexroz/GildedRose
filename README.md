Run and tested with Python `3.9.10` on Windows

Run tests with `python -m unittest test_gilded_rose.py -v`

Notes on the implementation:
1. Items are identified by name which means string matching. It would be more robust if items had a property for type.
1. Original implementation looks for specific items, while requirements seem general e.g. `Backstage passes to a TAFKAL80ETC concert` vs `"Backstage passes", like aged brie, increases in Quality as its SellIn value approaches` suggesting we should be looking for `Backstage passes*` instead of the specific `Backstage passes to a TAFKAL80ETC concert` matching. Leaving as is for this pass. (new requirement for conjured items does look for Conjured* - case insensivite - instead)
1. Case sensitivity of items matters, therefore leaving as is in lieu of specific instructions to change this.
1. 