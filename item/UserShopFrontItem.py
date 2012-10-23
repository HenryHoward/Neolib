from neolib.item.Item import Item
import logging

class UserShopFrontItem(Item):
    
    buyURL = None
    
    def buy(self):
        # Buy the item
        pg = self.usr.getPage("http://www.neopets.com/" + self.buyURL, vars = {'Referer': 'http://www.neopets.com/browseshop.phtml?owner=' + self.owner})
        
        # If it was successful a redirect to the shop is sent
        if "(owned by" in pg.content:
                return True
        elif "does not exist in this shop" in pg.content:
                return False
        else:
            logging.getLogger("neolib.item").exception("Unknown message when attempting to buy user shop item.", {'pg': pg})
            return False
