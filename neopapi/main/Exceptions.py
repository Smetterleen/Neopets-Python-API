
class OutOfMoneyException(Exception):
    def __init__(self, action):
        super(OutOfMoneyException, self).__init__('You ran out of Cash on Hand during the following action: ' + action)

class TooManyItemsException(Exception):
    def __init__(self):
        super(TooManyItemsException, self).__init__('You are carrying too many items')