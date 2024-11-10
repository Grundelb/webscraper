import requests


class NetworkConnector:

    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def load_listing_page(self, page_number: int, city_path: str) -> object:
        payload = {'page': page_number}
        url = self.base_url + city_path
        if page_number == 1:
            response = requests.get(url=url)
        else:
            response = requests.get(url=url, params=payload)
        return response
