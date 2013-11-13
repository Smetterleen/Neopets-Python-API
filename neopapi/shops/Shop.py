from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re
from neopapi.shops.Exceptions import NotEnoughMoneyInTillException,\
    ShopStockPageIndexError
from datetime import datetime

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

def stock_pages():
    """
    Returns the amount of pages of stock in the users shop
    
    """
    page = BROWSER.goto('market.phtml?type=your')
    pages_links = page.find_all('a', text=re.compile('\[\d*\-\d*\]'))
    # There are 2 page links for every page
    return int(len(pages_links)/2)

def amount_of_items_in_stock():
    page = BROWSER.goto('market.phtml?type=your')
    return int(page.find(text='Items Stocked : ').find_next('b').text)

def _items_on_page(page):
    if page < 1 or page > stock_pages():
        raise ShopStockPageIndexError()
    page = BROWSER._get('market.phtml?order_by=id&type=your&lim=%d' % (page * 30))
    trs_of_interest = page.find('form', action='process_market.phtml').find('tr').find_all_next('tr')[:30]
    item_trs = []
    for tr in trs_of_interest:
        if tr.find('input', {'name': re.compile('obj_id_\d*')}) is not None:
            item_trs.append(tr)
    items = []
    for item_tr in item_trs:
        item_info = item_tr.find_all('td')
        item = StockedItem(item_info[0].text, int(item_tr.find('input', {'name': re.compile('oldcost_\d*')})['value']), int(item_info[2].text), item_info[3].text)
        items.append(item)
    return items

def items_in_stock(page=None):
    """
    Returns the items currently in the users shop stock and the amount
    in stock. If a page is given, only the items on that page will be returned. 
    Page numbers start at 1.
    
    @return: e.g. [('eo codestone', 5)] -> There are 5 eo codestones in stock
    
    """
    if page is not None:
        return _items_on_page(page)
    items = []
    for page in range(1, stock_pages()+1):
        print(page)
        items.extend(_items_on_page(page))
    return items

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
    page = BROWSER.goto('market.phtml?type=your')
    size_string = page.find(text=re.compile('\(size \d*\)'))
    return re.search('\(size (\d*)\)', size_string).group(1)
    
def upgrade_shop(size=None):
    """
    Upgrades the users shop to the given size. If no size is given, the shop
    will be upgraded once
    
    """
    page = BROWSER.goto('market.phtml?type=edit')
    size_string = page.find(text=re.compile('.*Your shop is currently size.*')).next_element
    current_shop_size = int(size_string.text)
    if size is None:
        size = current_shop_size + 1
    while current_shop_size < size:
        page = BROWSER.post('process_market.phtml', {'type': 'upgrade'})
        size_string = page.find(text=re.compile('.*Your shop is currently size.*')).next_element
        current_shop_size = int(size_string.text)
    return current_shop_size
    

def np_in_till():
    """
    Returns the amount of np in the shops till
    
    """
    page = BROWSER.goto('market.phtml?type=till')
    size_string = page.find(text=re.compile('.*You currently have.*')).next_element
    return int(size_string.text.replace(',','').replace(' NP', ''))
    

def withdraw_from_till(amount=None, pin=None):
    """
    Withdraws the given amount from the shop till. If no amount is given, the till
    will be emptied completely
    
    """
    np_in_till_amount = np_in_till()
    if amount is not None:
        if amount > np_in_till_amount:
            raise NotEnoughMoneyInTillException()
    else:
        amount = np_in_till_amount
    BROWSER.goto('market.phtml?type=till')
    page = BROWSER.post('process_market.phtml', {'amount': amount,
                                                 'pin': pin,
                                                 'type': 'withdraw'})
    size_string = page.find(text=re.compile('.*You currently have.*')).next_element
    return int(size_string.text.replace(',','').replace(' NP', ''))

def sales_history():
    """
    Return the shops sales history in the from of a list containing the Sales in
    chronological order
    
    """
    page = BROWSER.goto('market.phtml?type=sales')
    sale_trs = page.find_all(text='Sales History')[1].find_all_next('p', limit=3)[2].find_all('tr')[1:-1]
    sales = []
    for sale_tr in sale_trs:
        sale_info = [el.text for el in sale_tr.find_all('td')]
        sale = Sale(datetime.strptime(sale_info[0], '%d/%m/%Y'), sale_info[1], sale_info[2], int(sale_info[3].replace(',','').replace(' NP','')))
        sales.append(sale)
        
    return sales
    

def clear_sales_history():
    """
    Clear the shops sales history
    
    """
    page = BROWSER.goto('market.phtml?type=sales')
    if page.find('input', value="Clear Sales History") is None:
        return False
    BROWSER.post('market.phtml', {'clearhistory': 'true',
                                  'type': 'sales'})
    return True
    
class StockedItem(object):
    
    def __init__(self, name, price, stock, item_type):
        self.name = name
        self.price = price
        self.stock = stock
        self.item_type = item_type
    
    def __str__(self):
        return '%s (%d in stock) is priced at %dnp' % (self.name, self.stock, self.price)
    
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
    
    def __str__(self):
        return '%s bought %s for %dnp on %s' % (self.buyer_name, self.item_name, self.price, self.date.strftime('%d/%m/%Y'))
