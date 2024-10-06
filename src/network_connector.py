import requests


class NetworkConnector:

    BASE_URL = 'https://www.halooglasi.com'
    ADD_URL = '/nekretnine/izdavanje-stanova'

    def __init__(self, city='novi-sad'):
        self.PATH_CITY = f'/{city}'

    def get_data(self, number: int):
        payload = {'page': number}
        url = self.BASE_URL+self.ADD_URL+self.PATH_CITY
        if number == 1:
            response = requests.get(url=url)
        else:
            response = requests.get(url=url, params=payload)
        return response
