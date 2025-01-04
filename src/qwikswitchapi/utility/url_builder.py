from urllib.parse import urljoin, quote_plus

class UrlBuilder:

    @staticmethod
    def build_get_all_device_status_url(base_uri: str, key: str) -> str:
        return urljoin(base_uri, f'state/{quote_plus(key)}/')

    @staticmethod
    def build_generate_api_keys_url(base_uri: str) -> str:
        return urljoin(base_uri, 'keys')

    @staticmethod
    def build_control_url(base_uri: str, key: str, device: str, level: int) -> str:
        return urljoin(base_uri,
                       f'control/{quote_plus(key)}/' +
                       f'?device={quote_plus(device)}&setlevel={level}')