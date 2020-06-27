""":mod:`AllStocks` -- Provides an interface for loading all neopets stocks

.. module:: AllStocks
   :synopsis: Provides an interface for loading all neopets stocks stocks
.. moduleauthor:: Henry Howard <henry.a.c.howard@gmail.com>
"""

from neolib.stock.Stock import Stock


FULL_STOCKS_URL = "http://www.neopets.com/stockmarket.phtml?type=list&full=true"


class AllStocks:

    """Defines an object containing every stock in the imaginary neopets stock
    market and the current information about it

    Attributes
        usr (User) -- Associated user
        stocks (List) -- A list of Stock() objects
        best_stocks (List) -- A list of Stock() objects representing the
            cheapest purchasable stocks for the day

    Methods:
        load() - scrapes the latest stock info from the website
        find_best() - populates self.best_stocks with those stocks that have a
            price closest to - but greater than - 15 np

    Example
        >>> a = AllStocks()
        >>> for stock in a.stocks:
        ...     print stock.company
        The Shoyru Company
        Peophin Water Parks!
        ...
        >>> a.best_stocks()
        >>> for stock in a.best_stocks:
        ...     print stock.price
        16
    """

    usr = None

    def _extract_row_data(self, row):
        """
        returns a dictionary like the following:
            {'ticker': 'UNIB',
            'company': 'Unis Beauty Salon',
            'volume': '0',
            'open': '8',
            'curr': '8',
            'change': '+0.00%'}
        """
        cells = row.find_all('td')
        data = [cell.text.strip() for cell in cells if cell.text != '']
        data = {self.legend[i].lower().strip(): data[i] for i in range(self.data_length)}
        return data

    def __init__(self, usr):
        self.usr = usr
        self.load()

    def load(self):
        """ Loads bargain stocks
        """
        self.pagedata = self.usr.getPage(FULL_STOCKS_URL)
        self.table = self.pagedata.find_all("table")[3].find_all('table')[4]
        rows = self.table.find_all('tr')
        self.legend = [
                cell.text.strip() for cell in
                rows[0].find_all('td')
                if cell.text != '' and cell.text != 'Logo'
                ]
        self.data_length = len(self.legend)

        self.stocks = [self._extract_row_data(row) for row in rows[1:]]
        self.stocks = [Stock(row) for row in self.stocks]

        self.purchasable_stocks = [s for s in self.stocks if s.curr_price >= 15]

    def find_best(self):
        """
        returns the cheapest purchasable stocks at the current time along with their
        price

        returns is of the form: [16, ['AAVL', 'CHIA', ...]]
        """
        cheapest_found = []
        benchmark = 15
        while not cheapest_found: #this evaluates to true for empty list
            for stock in self.stocks:
                if stock.curr_price == benchmark:
                    cheapest_found.append(stock.ticker)
            benchmark += 1
        self.best_stocks = []
        for stock in self.stocks:
            if stock.ticker in cheapest_found:
                self.best_stocks.append(stock)
