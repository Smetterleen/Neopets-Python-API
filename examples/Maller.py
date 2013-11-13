from neopapi.shops import Shop, ShopWizard
from datetime import datetime
from neopapi.core import Time
from neopapi.shops.Shop import StockedItem
from copy import copy

def run():
    
    # A list containing all the items that should be in the mall, their prices
    # relative to the lowest shop wizard price in the users section and the amount
    # that should always be present in the shop.
    #
    # e.g.  [{'name': 'eo codestone', 'markup': 12], ['zei codestone', -10, 5]]
    #   Stocks the default amount of eo codestones with a price 12% higher then the lowest shop wiz
    #   price, and 5 zei codestones with a price 10% lower then the lowest shop wiz price
    wanted_stock_list = [StockedItem('Buzzer', 500, 5), 
                         StockedItem('Greeble', 500, 1),
                         StockedItem('GORO', 500, 3),
                         StockedItem('Mallard', 500, 5)]
    
    needed_stock_list = []
    items_in_stock = {item.name: item for item in Shop.items_in_stock()}
    # Check which items are still needed in the shop stock
    for item in wanted_stock_list:
        if item.name in items_in_stock:
            if item.stock > items_in_stock[item.name].stock:
                needed_item = copy(item)
                needed_item.stock = item.stock - items_in_stock[item.name].stock
                needed_stock_list.append(needed_item)
        else:
            needed_stock_list.append(copy(item))
    
    # A dict containing the lowest price in the users shop segment as value, and the
    # name of the item as key
    shop_wizard_price_list = {}
    
    # Buy the needed items (and start creating a shop wizard price list)
    for item in needed_stock_list:
        search_results = ShopWizard.search(item.name)

    return Time.NST_tomorrow()
        
    
    