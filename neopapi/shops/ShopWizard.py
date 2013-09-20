from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re
from neopapi.shops.Exceptions import ItemOutOfStockException
from neopapi.main.Exceptions import OutOfMoneyException, TooManyItemsException

register_page('market.phtml?type=wizard',
              [],
              True)

def search(item_name):
    """
    Searches the shop wizard for the given item. 
    Returns an array of result, ordered by ascending price. The objects
    in the array are of the type 'WizardResult'.
    
    """
    BROWSER.goto('market.phtml?type=wizard')
    post_dict = {'criteria': 'exact',
                 'feedset': 0,
                 'max_price': 99999,
                 'min_price': 0,
                 'shopwizard': item_name,
                 'table': 'shop',
                 'type': 'process_wizard'
    }
        
    result_page = BROWSER.post('market.phtml', post_dict)
    if 'I did not find anything.  :(  Please try again and I will search elsewhere!' in result_page:
        return None
    
    result_trs = result_page.find('td', {'class': 'contentModuleHeaderAlt'}).find_parent('table').find_all('tr')
        
    results = []
    for result_tr in result_trs[1:]:
        bs = result_tr.find_all('b')
        username = bs[0].text
        price = int(re.sub('\D', '', bs[1].text))
        # Remove the first character of the link, because this is a '/' character, which
        # we do not need
        shop_link = result_tr.find('a')['href'][1:]
        stock = int(result_tr.find_all('td')[2].text)
        result = WizardResult(item_name, username, price, shop_link, stock)
        results.append(result)
            
    return results

class WizardResult:
    
    def __init__(self, item_name, username, price, shop_link, stock):
        self.item_name = item_name
        self.username = username
        self.price = price
        self.shop_link = shop_link
        self.stock = stock
    
    def buy(self):
        """
        This method will buy this item
        
        """
        shop_page = BROWSER._get(self.shop_link, referer='http://www.neopets.com/market.phtml')
        
        if 'Item not found!' in shop_page.text or 'There are no items for sale in this shop!' in shop_page.text:
            raise ItemOutOfStockException(self.item_name)
        
        item_link = shop_page.find('a', href=re.compile('buy_item.phtml\?lower\=0\&owner\=' + self.username + '.*'))['href']
        result_page = BROWSER._get(item_link)
        
        if 'The item you are trying to buy does not exist in this shop!' in result_page.text:
            raise ItemOutOfStockException(self.item_name)
        elif 'Not enough money' in result_page.text:
            raise OutOfMoneyException('Buying ' + self.item_name)
        elif 'Sorry, you can only carry a maximum of' in result_page.text:
            raise TooManyItemsException()
        return self.item_name
    
    def __repr__(self):
        return self.item_name + '@' + str(self.price) + 'np'