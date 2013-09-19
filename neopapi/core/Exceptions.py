
class CoreException(Exception):
    pass

class LoginRequiredException(CoreException):
    def __init__(self, url=None, msg=''):
        if url is None:
            return super(LoginRequiredException, self).__init__(msg)
        return super(LoginRequiredException, self).__init__('Login required for accessing url: ' + url + '\n' + msg)