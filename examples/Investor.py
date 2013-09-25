from neopapi.games import StockMarket
from neopapi.games.Exceptions import TooManyStocksBoughtException
from neopapi.core import Time
from datetime import timedelta
import secrets
import logging

logger = logging.getLogger(__name__)

last_stock_buy_date = None

def run():
    global last_stock_buy_time
    portfolio = StockMarket.portfolio()
    prices = StockMarket.get_stock_prices()
    if not last_stock_buy_time or last_stock_buy_date < Time.NST_date():
        logger.info('Buying stocks')
        price = 15
        while not last_stock_buy_time or last_stock_buy_date < Time.NST_date():
            logger.info('Looking for stocks priced at %dnp per share' % price)
            min_owned_stock = None
            for stock in [stock for stock in prices if stock.price == price]:
                if not min_owned_stock or portfolio.amount_owned(min_owned_stock.name) > portfolio.amount_owned(stock.name):
                    min_owned_stock = stock
            if min_owned_stock:
                try:
                    logger.info('Buying %s@%dnp' % (min_owned_stock.name, min_owned_stock.price))
                    StockMarket.buy_stock(min_owned_stock.name, 1000)
                    last_stock_buy_date = Time.NST_date()
                except TooManyStocksBoughtException:
                    logger.info('Failed: already bought stocks today')
                    last_stock_buy_date = Time.NST_date()
            else:
                logger.info('No stocks found at %dnp' % price)
                price += 1
    
    tm = Time.NST_time()
    if tm.hour > 13 and tm.hour < 23:
        logger.info('Waiting until tomorrow for updates to simulate sleep')
        return tm.replace(hour=23, minute=1, second=0)
    
    logger.info('Looking for stocks to sell')
    for stock in prices:
        if portfolio.amount_owned(stock.name) > 0 and stock.price > 60:
            amount_owned = portfolio.amount_owned(stock.name)
            logger.info('Selling %d shares of %s@%dnp' % (amount_owned, stock.name, stock.price))
            StockMarket.sell_stock(stock.name, amount_owned, pin=secrets.pin)
    next_update_time = tm - timedelta(minutes=(tm.minute % 30),
                                      seconds=tm.second,
                                      microseconds=tm.microsecond) + timedelta(minutes=31)
    logger.info('Waiting until %s for another stock update' % next_update_time.strftime("%X"))
    return next_update_time
    
        
    