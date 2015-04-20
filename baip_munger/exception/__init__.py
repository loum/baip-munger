__all__ = ['MungerConfigError']


class Error(Exception):
    def __init__(self, code=None, message=None):
        self.errno = code
        self.strerror = message

    def __str__(self):
        return '%d: %s' % (self.errno, self.strerror)


class MungerConfigError(Error):
    __error_msgs = {
        1000: 'Config file not found'
    }

    def __init__(self, code=None):
        msg = MungerConfigError.__error_msgs.get(code)
        super(MungerConfigError, self).__init__(code=code, message=msg)
