from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
from neopapi.shops.Exceptions import PageException

register_page('market.phtml?type=your',
              ['market.phtml?type=edit', 'market.phtml?type=till', 'market.phtml?type=sales',
               'quickstock.phtml'],
              True)
register_page('market.phtml?type=edit',
              ['market.phtml?type=edit', 'market.phtml?type=till', 'market.phtml?type=sales',
               'quickstock.phtml'])
register_page('market.phtml?type=till',
              ['market.phtml?type=edit', 'market.phtml?type=till', 'market.phtml?type=sales',
               'quickstock.phtml'])
register_page('market.phtml?type=sales',
              ['market.phtml?type=edit', 'market.phtml?type=till', 'market.phtml?type=sales',
               'quickstock.phtml'])   

def create_shop():
    """
    Creates a shop for the user.
    
    """
    # TODO: Implement
    raise NotImplementedError()

def item_pages():
    """
    Returns the amount of pages of stock in the users shop
    
    """
    stock_page = BROWSER.goto('market.phtml?type=your')
    pages = len(stock_page.find('form', action='market.phtml').find_previous('p').find_all('a')[1:])
    return pages

def items_in_stock(page=None):
    """
    Returns the items currently in the users shop stock and the amount
    in stock. If a page is given, only the items on that page will be returned. 
    Page numbers start at 1.
    
    @return: e.g. [('eo codestone', 5)] -> There are 5 eo codestones in stock
    
    """
    stock_page = BROWSER.goto('market.phtml?type=your')
    pages = stock_page.find('form', action='market.phtml').find_previous('p').find_all('a')[1:]
    if page is not None:
        if page > len(pages):
            raise PageException()
        elif page != 1:
            stock_page_link = pages[page-1]['href']
            stock_page = BROWSER._get(stock_page_link)
        return _get_items_from_stock_page(stock_page)
    
    items_in_stock = []
    for page in range(len(pages)):
        if page != 0:
            stock_page_link = pages[page]['href']
            print(stock_page_link)
            stock_page = BROWSER._get(stock_page_link)
        items_in_stock.extend(_get_items_from_stock_page(stock_page))
    return items_in_stock

def _get_items_from_stock_page(stock_page):
    item_trs = stock_page.find('form', action='process_market.phtml').find_all('tr')[1:]
    print('\n'.join([str(x) for x in item_trs]))
    return []

def update_item_pricing(item_price_list, page=None, pin=None):
    """
    Updates the pricing on the given items. If a page is given, only the
    items on that page will be updated. If an item in the list is not on
    the given page, it will be ignored.
    If no page is given, each page will be checked for the given items, until
    all items are found, or the final page is reached. Unfound items will
    be ignored.
    Objects in the 'item_price_list' argument should be of type 'ItemPricing'
    
    """
    # TODO: Implement
    raise NotImplementedError()

def size():
    """
    Returns the current size of the users shop
    
    """
    # TODO: Implement
    raise NotImplementedError()
    
def upgrade_shop(size=None):
    """
    Upgrades the users shop to the given size. If no size is given, the shop
    will be upgraded once
    
    """
    # TODO: Implement
    raise NotImplementedError()

def np_in_till():
    """
    Returns the amount of np in the shops till
    
    """
    # TODO: Implement
    raise NotImplementedError()

def withdraw_from_till(amount=None, pin=None):
    """
    Withdraws the given amount from the shop till. If no amount is given, the till
    will be emptied completely
    
    """
    # TODO: Implement
    raise NotImplementedError()

def sales_history():
    """
    Return the shops sales history in the from of a list containing the Sales in
    chronological order
    
    """
    # TODO: Implement
    raise NotImplementedError()

def clear_sales_history():
    """
    Clear the shops sales history
    
    """
    # TODO: Implement
    raise NotImplementedError()

class ItemPricing(object):
    
    def __init__(self, item_name, price, remove=False):
        self.item_name = item_name
        self.price = price
        self.remove = remove
        
class Sale(object):
    
    def __init__(self, date, item_name, buyer_name, price):
        self.date = date
        self.item_name = item_name
        self.buyer_name = buyer_name
        self.price = price