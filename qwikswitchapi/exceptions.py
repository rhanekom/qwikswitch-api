class QSException(Exception):
    """
    Base exception raised by the Qwikswitch API.
    Source exceptions are chained.
    """
    pass

class QSAuthException(QSException):
    """
    Exception raised by the Qwikswitch API when authentication fails.
    Source exceptions are chained.
    """
    pass

class QSRequestFailedException(QSException):
    """
    Exception raised by the Qwikswitch API when a request fails.
    Source exceptions are chained.
    """
    pass

class QSRequestErrorException(QSException):
    """
    Exception raised by the Qwikswitch API when a request fails.
    Source exceptions are chained.
    """
    pass