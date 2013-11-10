
class LockedOutException(Exception):
    def __init__(self, username):
        super(LockedOutException, self).__init__('You have entered a wrong password too many times for username %s and can\'t login anymore for an hour' % username)

class WrongUsernameException(Exception):
    def __init__(self, username):
        super(WrongUsernameException, self).__init__('You have given a non-existant username: %s' % username)
class WrongPasswordException(Exception):
    def __init__(self, username):
        super(WrongPasswordException, self).__init__('Wrong password given for username: %s' % username)

class OutOfMoneyException(Exception):
    def __init__(self, action):
        super(OutOfMoneyException, self).__init__('You ran out of Cash on Hand during the following action: ' + action)

class TooManyItemsException(Exception):
    def __init__(self):
        super(TooManyItemsException, self).__init__('You are carrying too many items')

class ActionNotPossibleException(Exception):
    def __init__(self, item_name, action):
        super(ActionNotPossibleException, self).__init__('Action \'' + action + '\' not allowed for item: ' + item_name)