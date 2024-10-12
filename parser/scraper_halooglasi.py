from bs4 import BeautifulSoup
from parser.base_scraper import BaseScraper


class HalooglasiScraper(BaseScraper):

    BASE_URL = 'https://www.halooglasi.com/nekretnine/izdavanje-stanova'

    def fetch_apartment_listings(self, page_content) -> list[str]:
        soup = BeautifulSoup(page_content.content, 'lxml')
        return soup.find_all('div', class_='row')

    def get_apartment_title(self, apartment) -> str:
        product_title = apartment.find('h3', class_='product-title')
        title = None
        if product_title:
            title = product_title.find('a').text.strip()
        return title

    def get_apartment_link(self, apartment) -> str:
        product_title = apartment.find('h3', class_='product-title')
        link_to_apartment = None
        if product_title:
            link_to_apartment = product_title.find('a')['href']
        return link_to_apartment

    def get_rooms_number(self, apartment) -> str:
        product_features = apartment.find('ul', class_='product-features')
        rooms = None
        if product_features:
            features_items = product_features.find_all('li', class_='col-p-1-3')
            if len(features_items) >= 2:
                rooms_div = features_items[1].find('div', class_='value-wrapper')
                if rooms_div:
                    rooms = rooms_div.get_text().replace('Broj soba', '')[:3]
                    return rooms
        return rooms

    def get_apartment_city(self, apartment) -> str:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        city = None
        if subtitle_places:
            places_items = subtitle_places.find_all('li')
            places = [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
            if len(places) >= 3:
                city = places[0]
            elif len(places) >= 2:
                city = places[0]
        return city

    def get_apartment_district(self, apartment) -> str:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        district = None
        if subtitle_places:
            places_items = subtitle_places.find_all('li')
            places = [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
            if len(places) >= 3:
                district = places[2]
            elif len(places) >= 2:
                district = places[1]
        return district

    def get_apartment_price(self, apartment):
        price_tag = apartment.find('div', class_='central-feature')
        price = None
        if price_tag:
            price = price_tag.find('span').text
        return price
