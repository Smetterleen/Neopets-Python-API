
class BankException(Exception):
    pass

class WrongPINException(Exception):
    pass

class ShopWizardException(Exception):
    pass

class ItemOutOfStockException(ShopWizardException):
    def __init__(self, item_name):
        super(ItemOutOfStockException, self).__init__('Item is out of stock: ' + item_name)

class UserShopException(Exception):
    pass

class PageException(UserShopException):
    pass