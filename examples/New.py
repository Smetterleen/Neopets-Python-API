from neopapi.main import Inventory
from neopapi.explore.world.island import TrainingSchool
from neopapi.shops import ShopWizard, Shop
from neopapi.explore.world.island.Exceptions import StatTooHighException
from neopapi.core import Time
from neopapi.shops.Exceptions import ItemOutOfStockException
import logging
import secrets
from neopapi.core.Time import NST_tomorrow

logger = logging.getLogger(__name__)

def run():
    print([str(el) for el in Shop.items_in_stock()])
    return NST_tomorrow()