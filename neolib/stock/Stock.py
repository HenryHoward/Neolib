""":mod:`Stock` -- Provides an interface for Neopets stocks

.. module:: Stock
   :synopsis: Provides an interface for Neopets stocks
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""
def clean_numeric(string_value):
    # Clean commas
    cleaned = string_value.replace(',', '')
    # Clean percent signs
    cleaned = cleaned.replace('%', '')
    return cleaned


class Stock:

    """ An class representing a Neopets stock

    Attributes
       ticker
       open
       current price
       qty || volume
       % change
       company      -- maybe null
       chg          -- maybe null
       paid         -- maybe null
       mkt value    -- maybe null
    """

    def __init__(self, data):
        """ Initialized with data from an HTML row """
        # Required Data
        self.ticker = data['ticker'].split()[0]
        self.volume = int(clean_numeric(data.get('volume', data.get('qty', ''))))
        self.open_price = int(clean_numeric(data['open']))
        self.curr_price = int(clean_numeric(data.get('curr')))
        self.percent_change = float(clean_numeric(data['change'])) / 100.

        # Optional Data
        self.company = data.get('company', '')
        self.absolute_change = data.get('chg')
        self.paid = data.get('paid')
        self.mkt_value = data.get('mkt value')

