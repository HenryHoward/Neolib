""":mod:`CurrentFunds` -- Gets how much liquid neopoint the user has

.. module:: CurrentFunds
   :synopsis: Gets how much liquid neopoint the user has
.. moduleauthor:: Henry Howard <henry.a.c.howard@gmail.com>
"""

import logging

class CurrentFunds:

    """Tells how much liquid neopoint the user has

    Attributes
        usr (User object) - the user in question
        value (int) - number of available neopoints

    Methods
        load() - updates the self.amount attribute

    Example
       >>> usr.current_funds.load()
       >>> usr.current_funds.amount
       100000
    """

    def __init__(self, usr):
        self.amount = None

        if not usr:
            return
        self.usr = usr

    def load(self):
        """ Scrapes the number of available neopoints
        """
        #arbitrarily chose the inventory page as the one to visit here:
        pg = self.usr.getPage("http://www.neopets.com/inventory.phtml")
        amount = int(pg.select('#npanchor')[0].text.replace(',',''))

        self.amount = amount
