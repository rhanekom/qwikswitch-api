from requests import RequestException

from src.qwikswitchapi.qsexception import QSException

class ResponseParser:

    @staticmethod
    def get_failure_message(resp) -> str:
        """
        Returns a formatted message indicating the request failed
        :param resp: The response object
        :return: A formatted message indicating the request failed
        """
        request_url = resp.request.url
        return f'Failed to call {request_url}.  Status code: "{resp.status_code}", body: "{resp.text}"'

    @staticmethod
    def raise_request_failure(url, ex: RequestException):
        """
        Raises a QSException indicating the request failed
        :param url: The URL of the request
        :param ex: The exception that was raised
        :raises QSException: Indicating the request failed, chained with the original exception.
        """
        raise QSException(f'Request to {url} failed: {str(ex)}') from ex

    @staticmethod
    def raise_request_error(resp):
        """
        Raises a QSException indicating the request failed
        :param resp: The response object
        :raises QSException: Indicating the request failed, with the body of the response.
        """
        raise QSException(ResponseParser.get_failure_message(resp))