"""Exceptions for the Qwikswitch API."""


class QSError(Exception):
    """
    Base exception raised by the Qwikswitch API.

    Source exceptions are chained.
    """


class QSAuthError(QSError):
    """
    Exception raised by the Qwikswitch API when authentication fails.

    Source exceptions are chained.
    """


class QSRequestFailedError(QSError):
    """
    Exception raised by the Qwikswitch API when a request fails.

    Source exceptions are chained.
    """


class QSRequestError(QSError):
    """
    Exception raised by the Qwikswitch API when a request fails.

    Source exceptions are chained.
    """


class QSResponseParseError(QSRequestError):
    """
    Exception raised by the Qwikswitch API when validations fail on a response.

    Source exceptions are chained.
    """
