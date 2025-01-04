from requests import RequestException

from src.qwikswitchapi.qs_exception import QSException

class ResponseParser:

    @staticmethod
    def get_failure_message(resp) -> str:
        request_url = resp.request.url
        return f'Failed to call {request_url}.  Status code: "{resp.status_code}", body: "{resp.text}"'

    @staticmethod
    def raise_request_failure(url, ex: RequestException):
        raise QSException(f'Request to {url} failed: {str(ex)}') from ex

    @staticmethod
    def raise_request_error(resp):
        raise QSException(ResponseParser.get_failure_message(resp))