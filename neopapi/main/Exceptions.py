
class OutOfMoneyException(Exception):
    def __init__(self, action):
        super(OutOfMoneyException, self).__init__('You ran out of Cash on Hand during the following action: ' + action)