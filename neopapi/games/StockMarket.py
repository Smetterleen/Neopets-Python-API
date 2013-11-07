from neopapi.core.browse.Browser import BROWSER
import re
from bs4 import BeautifulSoup
from neopapi.games.Exceptions import StockException,\
    StockNotInPortfolioException, TooManyStocksBoughtException
from neopapi.main.Exceptions import OutOfMoneyException
from neopapi.shops.Exceptions import WrongPINException
from neopapi.core.browse import register_page

register_page('stockmarket.phtml',
              ['stockmarket.phtml?type=portfolio', 'stockmarket.phtml?type=buy'])

def portfolio():
    """
    Returns all the stocks currently in the users portfolio
    
    """
    page = BROWSER.goto('stockmarket.phtml?type=portfolio')
    stock_list = [stock_link.find_parent('tr') for stock_link in page.find_all('a', href=re.compile('.*company.*'))]
    owned_stocks = Portfolio()
    for stock_element in stock_list:
        purchases = stock_element.find_next_sibling('tr').find('table').find_all('tr')[2:]
        purchase_list = []
        for purchase in purchases:
            tds = purchase.find_all('td')
            amount = int(tds[0].text.replace(',',''))
            buy_price = int(tds[1].text)
            number = re.sub('\D', '', tds[-1].find('input')['name'])
            purchase_list.append(Purchase(number, amount, buy_price))
        parts = stock_element.find_all('td')
        name = parts[1].find('a').text
        owned_stocks[name] = purchase_list
    return owned_stocks

def buy_stock(stock_name, amount=1000):
    """
    Buys the given amount of the given stock
    
    """
    page = BROWSER.goto('stockmarket.phtml?type=buy')
    stocks = get_stock_prices()
    if stock_name in [stock.name for stock in stocks]:
        ref_ck = page.find('input', attrs={'name': '_ref_ck'})
        post_dict = {'_ref_ck': ref_ck['value'],
                     'amount_shares': str(amount),
                     'ticker_symbol': stock_name,
                     'type': 'buy'}
        bought_page = BROWSER.post('process_stockmarket.phtml', post_dict)
        if 'Sorry, that would take you over the daily purchase limit of 1000  shares' in bought_page.text:
            raise TooManyStocksBoughtException(stock_name, amount)
        elif 'You cannot afford that!' in bought_page.text:
            raise OutOfMoneyException()
    return portfolio()
    

def sell_stock(stock_name, amount=None, pin=None):
    """
    Sells the given amount of the given stock. If no amount
    is given, all the stocks of the given name will be sold.
    
    """
    page = BROWSER.goto('stockmarket.phtml?type=portfolio')
    stocks = portfolio()
    if stock_name in stocks:
        purchases = stocks[stock_name]
        amount_owned = sum([purchase.amount for purchase in purchases])
        if amount_owned < amount:
            raise StockNotInPortfolioException(stock_name, amount)
            
        ref_ck = page.find('input', attrs={'name': '_ref_ck'})
        post_dict = {'_ref_ck': ref_ck['value'],
                     'type': 'sell'}
        
        amount_left_to_sell = amount
        for portf_stock_name, purchases in stocks.items():
            for purchase in purchases:
                post_key = 'sell[' + portf_stock_name + '][' + purchase.number + ']'
                if portf_stock_name == stock_name and amount_left_to_sell > 0:
                    post_dict[post_key] = min(amount_left_to_sell, purchase.amount)
                    amount_left_to_sell -= min(amount_left_to_sell, purchase.amount)
                else:
                    post_dict[post_key] = ''
        
        if 'Enter your PIN:' in page.text:
            if pin is None:
                raise WrongPINException('PIN is required to sell stocks')
            post_dict['pin'] = pin
                
        result_page = BROWSER.post('process_stockmarket.phtml', post_dict)
            
        if 'Sorry, but the PIN we have stored is not matching the one you entered' in result_page.text:
            raise WrongPINException('Wrong pin given while trying to sell stocks')
        
        return portfolio()
    else:
        raise StockNotInPortfolioException(stock_name, amount)

def get_stock_prices():
    """
    Returns a list containing all Stock in the stock market and
    their price
    
    """
    if 'stockmarket.phtml' in BROWSER.last_visited_url():
        page = BROWSER.last_visited_page()
    else:
        page = BROWSER.goto('stockmarket.phtml')
    
    stock_list = BeautifulSoup(page.find('script', text=re.compile('.*marquee.*')).text.lstrip('document.write(\'').rstrip('\');'))
    stocks = []
    for stock in [b_tag.text for b_tag in stock_list.find_all('b')]:
        stock_info = stock.split()
        if stock_info[0] in [stock.name for stock in stocks]:
            break
        stock = Stock(name=stock_info[0], price=int(stock_info[1]), change=stock_info[2])
        stocks.append(stock)
    return stocks

class Stock(object):
    
    def __init__(self, name, price, change):
        self.name = name
        self.price = price
        self.change = change
    
    def __repr__(self):
        return self.name

class Purchase(object):
    
    def __init__(self, number, amount, price):
        self.number = number
        self.amount = amount
        self.price = price
    
    def __repr__(self):
        return str(self.number) + '@' + str(self.price) + 'np'

class Portfolio(dict):
    
    def amount_owned(self, stock_name):
        try:
            stock_purchases = self[stock_name]
            return sum([stock_purchase.amount for stock_purchase in stock_purchases])
        except KeyError:
            return 0
        