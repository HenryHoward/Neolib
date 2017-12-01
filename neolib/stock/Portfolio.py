""":mod:`Portfolio` -- Provides an interface for loading a user's stock portfolio

.. module:: Portfolio
   :synopsis: Provides an interface for loading a user's stock portfolio
.. moduleauthor:: Kelly McBride <kemcbride28@gmail.com>
"""

from Stock import Stock
import requests

class Portfolio:

    """Provides an interface for loading a user's stock portfolio

    Attributes
       usr (User) -- Associated user
       stocks (List) -- The User's Stocks

    Initialization
       Portfolio(usr)

       Initializes the class with the user
       and gets their portfolio.

       Parameters
          usr (User) -- User whose portfolio to access

    Example
       >>> p = Portfolio(usr)
       >>> for stock in p.stocks:
       ...     print stock.company
       The Shoyru Company
       Peophin Water Parks!
       ...
    """

    usr = None

    def extract_row_data(self, row):
        cells = row.find_all('td')
        data = [cell.text.strip() for cell in cells if cell.text != '']
        data = {self.legend[i].lower(): data[i] for i in range(len(self.legend))}
        return data

    def verify_sell_input_tag(self, input_tag):
        return (
            type(i.get('name')) == unicode and
            i.get('name').startswith('sell[{}]'.format(ticker))
            )

    def tickers(self):
        return [s.ticker for s in self.stocks]

    def __init__(self, usr):
        self.usr = usr
        self.load()  # Load automatically, I don't wanna have to call load...

    def load(self):
        """ Loads the user's portfolio
        """
        pagedata = self.usr.getPage("http://www.neopets.com/stockmarket.phtml?type=portfolio")
        # self.legend = self.extract_row_data(rows[1])
        self.legend = ['Ticker','Open','Curr','Chg','Qty','Paid','Mkt Value','Change']
        self.data_length = len(self.legend)

        # Arbitrarily, they have some rows with style=display:none but we'll just
        # take the ones that have a background color set.
        rows = [e for e in pagedata.find_all('tr') if e.has_attr('bgcolor') and (e.get('bgcolor') == '#EEEEFF' or e.get('bgcolor') == '#FFFFFF')]
        self.stocks = [self.extract_row_data(row) for row in rows]
        # Filter rows that are the wrong length - we get the sub-dropdown-rows, too
        self.stocks = [Stock(row) for row in self.stocks if len(row) == len(self.legend)]

    def buy(self, ticker, amount):
        """ Buy the given amount of stock identified by ticker (if you have the funds!)
        """
        pagedata = self.usr.getPage("http://www.neopets.com/stockmarket.phtml?type=buy")
        form = pagedata.form(action='process_stockmarket.phtml', method='post')

        # We need 4 things in our form data:
        form['ticker_symbol'] = ticker
        form['amount_shares'] = amount
        form['type'] = 'buy'
        form['_ref_ck'] = [
                i for i in pagedata.find_all('input')
                if i.get('name') == '_ref_ck'
                ][0].get('value')
        result = form.submit()

    def sell(self, ticker, amount):
        """ Sell the given amount of stock identified by ticker (if you have the shares!)
        """
        pagedata = self.usr.getPage("http://www.neopets.com/stockmarket.phtml?type=portfolio")
        # 1 - this doesn't seem to work anymore
        # 2 - it searches the entire page instead of like a content div
        # re: 1. i'm assuming that the unicode check is probably what's doing it...
        inputs = [
                i for i in pagedata.find_all('input')
                if self.verify_sell_input_tag(i)
                ]
        remaining_input = amount
        payload = {}
        for i in inputs:
            # Think! clean_numeric should be a common function for me!          
            capacity = int(i.parent.parent.find('td').string.replace(',',''))
            if capacity >= remaining_input:
                payload[i['name']] = remaining_input
                i['value'] = remaining_input
                break
            payload[i['name']] = capacity
            i['value'] = capacity
            remaining_input -= capacity

        payload['type'] = 'sell'
        payload['_ref_ck'] = [
                i for i in pagedata.find_all('input')
                if i.get('name') == '_ref_ck'
                ][0].get('value')
        result = self.usr.session.post('http://www.neopets.com/process_stockmarket.phtml', data=payload)

        # Detect whether it was successful by telling if that text that we sold is in it
        if "successful transaction" in result.content:
            print "Successful sale!"
        return result


