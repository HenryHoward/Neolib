""":mod:`UserInventory` -- Provides an interface for a user inventory

.. module:: UserInventory
   :synopsis: Provides an interface for a user inventory
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.exceptions import parseException
from neolib.exceptions import invalidUser
from neolib.inventory.Inventory import Inventory
from neolib.item.Item import Item
import logging

class UserInventory(Inventory):
     
    """Represents a user's inventory
    
    Sub-classes the Inventory class to provide an interface for a user's
    inventory. Will automatically populate itself with all items
    in a user's inventory upon initialization.
        
    Example
       >>> usr.inventory.load()
       >>> for item in usr.inventory.items():
       ...     print item.name
       Blue Kougra Plushie
       Lu Codestone
       ...
    """
     
    usr = None
     
    def __init__(self, usr):
        if not usr:
            raise invalidUser
            
        self.usr = usr
        self.items = {}
        self.cash_items = {}
            
    def parse_items(self, element):
        """Parse the items out of a given element and return the item dict"""
        inv = {}
        for row in element.table.find_all("tr"):
            for item in row.find_all("td"):
                name = item.text
                
                # Some item names contain extra information encapsulated in paranthesis
                if "(" in name:
                    name = name.split("(")[0]
                
                # note: What if you have more than one of an item?
                # a: [i guess on reload, the item will still be present]
                tmpItem = Item(name)
                tmpItem.id = item.a['onclick'].split("(")[1].replace(");", "")
                tmpItem.img = item.img['src']
                tmpItem.desc = item.img['alt']
                tmpItem.usr = self.usr
                inv[name] = tmpItem
        return inv

    def load(self):
        """Loads a user's inventory
       
       Queries the user's inventory, parses each item, and adds 
       each item to the inventory. Note this class should not be 
       used directly, but rather usr.inventory should be used to 
       access a user's inventory.
       
       Parameters
          usr (User) - The user to load the inventory for
          
       Raises
          invalidUser
          parseException
        """
        pg = self.usr.getPage("http://www.neopets.com/objects.phtml?type=inventory")
        
        # Indicates an empty inventory
        if "You aren't carrying anything" in pg.content:
            return
        
        try:
            self.items = self.parse_items(pg.find_all("td", "contentModuleContent")[0])
            self.cash_items = self.parse_items(pg.find_all("td", "contentModuleContent")[1])

        except Exception:
            logging.getLogger("neolib.inventory").exception("Unable to parse user inventory.", {'pg': pg})
            raise parseException
