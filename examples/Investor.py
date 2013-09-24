from neopapi.games import StockMarket
from neopapi.games.Exceptions import TooManyStocksBoughtException
from neopapi.core import Time
from datetime import timedelta
import secrets

bought_stocks = False

def run():
    global bought_stocks
    portfolio = StockMarket.portfolio()
    prices = StockMarket.get_stock_prices()
    if not bought_stocks:
        print('Buying stocks')
        price = 15
        while not bought_stocks:
            print('Looking for stocks priced at %dnp per share' % price)
            min_owned_stock = None
            for stock in [stock for stock in prices if stock.price == price]:
                if not min_owned_stock or portfolio.amount_owned(min_owned_stock.name) > portfolio.amount_owned(stock.name):
                    min_owned_stock = stock
            if min_owned_stock:
                try:
                    print('Buying %s@%dnp' % (min_owned_stock.name, min_owned_stock.price))
                    StockMarket.buy_stock(min_owned_stock.name, 1000)
                    bought_stocks = True
                except TooManyStocksBoughtException:
                    print('Failed: already bought stocks today')
                    bought_stocks = True
            else:
                print('No stocks found at %dnp' % price)
                price += 1
    
    print('Looking for stocks to sell')
    for stock in prices:
        if portfolio.amount_owned(stock.name) > 0 and stock.price > 60:
            amount_owned = portfolio.amount_owned(stock.name)
            print('Selling %d shares of %s@%dnp' % (amount_owned, stock.name, stock.price))
            StockMarket.sell_stock(stock.name, amount_owned, pin=secrets.pin)
    tm = Time.NST_time()
    next_update_time = tm - timedelta(minutes=(tm.minute % 30),
                                      seconds=tm.second,
                                      microseconds=tm.microsecond) + timedelta(minutes=31)
    print('Waiting until %s for another stock update' % next_update_time.strftime("%X"))
    return next_update_time
    
        
    