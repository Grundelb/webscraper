import requests


class NetworkConnector:

    def __init__(self, base_url: str, city='novi-sad'):
        self.base_url: str = base_url
        self.path_city = f'/{city}'

    def load_listing_page(self, page_number: int) -> object:
        payload = {'page': page_number}
        url = self.base_url + self.path_city
        if page_number == 1:
            response = requests.get(url=url)
        else:
            response = requests.get(url=url, params=payload)
        return response
