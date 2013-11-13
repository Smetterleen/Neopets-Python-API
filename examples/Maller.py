from neopapi.shops import Shop
from datetime import datetime
from neopapi.core import Time

def run():
    
    # A list containing all the items that should be in the mall, their prices
    # relative to the lowest shop wizard price in the users section and the amount
    # that should always be present in the shop.
    #
    # e.g.  [{'name': 'eo codestone', 'markup': 12], ['zei codestone', -10, 5]]
    #   Stocks the default amount of eo codestones with a price 12% higher then the lowest shop wiz
    #   price, and 5 zei codestones with a price 10% lower then the lowest shop wiz price
    wanted_stock_list = []
    
    items_in_stock = Shop.items_in_stock()
    items_in_stock_dict = {name: item for name, item in [(item.name, item) for item in items_in_stock]}
    
    for wanted_item in wanted_stock_list:
        if wanted_item.name not in items_in_stock_dict or wanted_item.stock > items_in_stock[wanted_item.name].stock:
            # Stock needs to be filled
            pass
    
    # All items are now sufficiently stocked
    
            
            
        
    
    print('Stock pages: %d' % Shop.item_pages())
    print(Shop.items_in_stock())
    
    return Time.NST_tomorrow()
        
    
    