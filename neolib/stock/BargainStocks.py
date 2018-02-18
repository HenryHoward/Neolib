""":mod:`BargainStocks` -- Provides an interface for loading bargain stocks

.. module:: BargainStocks
   :synopsis: Provides an interface for loading bargain stocks
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from Stock import Stock

class BargainStocks:

    """Provides an interface for loading bargain stocks

    Attributes
       usr (User) -- Associated user
       stocks (List) -- The Bargain Stocks

    Initialization
       BargainStocks(usr)

       Initializes the class with the current user
       and gets the bargain stocks.

       Parameters
            usr - current User. (NOT NECESSARY!)

    Example
       >>> b = BargainStocks()
       >>> for stock in b.stocks:
       ...     print stock.company
       The Shoyru Company
       Peophin Water Parks!
       ...
    """

    usr = None
    BARGAIN_STOCKS_URL = "http://www.neopets.com/stockmarket.phtml?type=list&search=+-invalid_characters-+&bargain=true"

    def extract_row_data(self, row):
        cells = row.find_all('td')
        data = [cell.text.strip() for cell in cells if cell.text != '']
        data = {self.legend[i].lower().strip(): data[i] for i in range(self.data_length)}
        return data

    def __init__(self, usr):
        self.usr = usr
        self.load()  # Load automatically, I don't wanna have to call load...

    def load(self):
        """ Loads bargain stocks
        """
        self.pagedata = self.usr.getPage(BARGAIN_STOCKS_URL)
        self.table = self.pagedata.find_all("table")[3].find_all('table')[4]
        rows = self.table.find_all('tr')
        self.legend = [
                cell.text.strip() for cell in
                rows[0].find_all('td')
                if cell.text != '' and cell.text != 'Logo'
                ]
        self.data_length = len(self.legend)

        self.stocks = [self.extract_row_data(row) for row in rows[1:]]
        self.stocks = [Stock(row) for row in self.stocks]

        self.purchasable_stocks = [s for s in self.stocks if s.curr_price >= 15]

    def tickers(self):
        return [s.ticker for s in self.stocks]
