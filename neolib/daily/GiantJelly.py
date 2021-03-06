""":mod:`GiantJelly` -- Contains the GiantJelly class

.. module:: GiantJelly
   :synopsis: Contains the GiantJelly class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.daily.Daily import Daily
from neolib.exceptions import dailyAlreadyDone
from neolib.exceptions import parseException
import logging

class GiantJelly(Daily):
    
    """Provides an interface for the Giant Jelly daily
    
    For a more detailed description, please refer to the Daily class.
    """
    
    def play(self):
        pg = self.player.getPage("http://www.neopets.com/jelly/jelly.phtml")
        
        form = pg.form(action="jelly.phtml")
        pg = form.submit()
        
        if "NO!" in pg.content:
            raise dailyAlreadyDone
        
        try:
            parts = pg.find_all("p")
        
            self.img = parts[2].img['src']
            self.prize = parts[3].b.text
            
            self.win = True
        except Exception:
            logging.getLogger("neolib.daily").exception("Could not parse Giant Jelly daily.", {'pg': pg})
            raise parseException
        
    def getMessage(self):
        if self.win:
            return "You recieved a " + self.prize + "!"
        else:
            return "You did not win anything"
