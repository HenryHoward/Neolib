"""This is an example script for purchasing as much cheap stocks as possible
from the neopean stock market
"""

import math
from neolib.user.User import User
from neolib.stock.AllStocks import AllStocks
from neolib.user.CurrentFunds import CurrentFunds
from neolib.stock.Portfolio import Portfolio

#Initialise the User() object with your username and password then log in
usr = User("YOUR USERNAME HERE", "YOUR PASSWORD HERE")
usr.login()

#Load information about the user's current funds into User object
usr.current_funds.load()
available_funds = usr.current_funds.amount

#initialise an AllStocks() object which contains information about the current
#state of the neopean stock market:
stock_market = AllStocks(usr)

#Use the find_best() method of AllStocks to get the cheapest purchasable stocks
#for the day
stock_market.find_best()
to_buy = stock_market.best_stocks
ticker = to_buy[0].ticker #[0] because we only need one cheap stock
price = to_buy[0].curr_price

#Stocks are bought and sold using a Portfolio() object:
stock_portfolio = Portfolio(usr)

#Buy the maximum number of our chosen stock
stock_portfolio.buy(ticker, min(1000, math.floor(available_funds/price)))
