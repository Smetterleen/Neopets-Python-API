# Small wrapper around the shop wizard
from neopapi.shops import ShopWizard

def search(self, item_name):
    return ShopWizard.search(item_name)
    
def deep_search(self, item_name):
    results = []
    for _ in range(5):
        results.extend(ShopWizard.search(item_name))
    cheapest_results = sorted()
    # TODO:
    pass
    
def exhaustive_search(self, item_name):
    # TODO:
    pass