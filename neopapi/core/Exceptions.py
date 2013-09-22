
class CoreException(Exception):
    pass

class EndOfHistoryException(Exception):
    def __init__(self):
        super(EndOfHistoryException, self).__init__('Browser can\'t go back any further in history')

class LoginRequiredException(CoreException):
    def __init__(self, url=None, msg=''):
        if url is None:
            return super(LoginRequiredException, self).__init__(msg)
        return super(LoginRequiredException, self).__init__('Login required for accessing url: ' + url + '\n' + msg)