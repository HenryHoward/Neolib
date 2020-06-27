""":mod:`Inventory` -- Provides an interface for a Neopets inventory

.. module:: Inventory
   :synopsis: Provides an interface for a Neopets inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

class Inventory(object):
    """Represents a Neopets inventory

    This class is designed to be sub-classed by other
    classes that represent a Neopets inventory. Such
    examples include user inventory, safety deposit
    box, and shop inventory. The main purpose of this
    class is to provide a common interface for all
    inventories.

    Attributes:
        items (list): should be a list of Item objects but is currently a
        dictionary

    TODO: fix items so that it can have more than one item of each name. Perhaps
        a list? How to handle that retrieving items from inventory may return
        more than one value?
    """

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        self.items.pop(key)

    def __contains__(self, key):
        if key in self.items:
            return True
        else:
            return False

    def __iter__(self):
        for item in self.items: #item is the dictionary key in this case
            yield self.items[item]

    def __len__(self):
        return len(self.items)

    def empty(self):
        return bool(len(self.items))
