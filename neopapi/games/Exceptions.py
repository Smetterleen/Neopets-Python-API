class StockException(Exception):
    pass

class TooManyStocksBoughtException(StockException):
    def __init__(self, stock_name, amount):
        super(StockException, self).__init__('Bought too many stocks today for this purchase: %d of %s' % (amount, stock_name))

class NoSuchStockException(StockException):
    def __init__(self, stock_name):
        super(StockException, self).__init__('Stock does not exist: %s' % stock_name)

class StockNotInPortfolioException(StockException):
    def __init__(self, stock_name, amount):
        super(StockException, self).__init__('You do not have %d stocks of %s in your portfolio' % (amount, stock_name))