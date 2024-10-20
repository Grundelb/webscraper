from bs4 import BeautifulSoup
from parser.abstract_scraper import AbstractScraper
from typing import Optional
import parser_exceptions
import logging


class HalooglasiScraper(AbstractScraper):
    BASE_URL = 'https://www.halooglasi.com/nekretnine/izdavanje-stanova'

    def fetch_apartment_listings(self, page_content) -> list[AbstractScraper.ApartmentPageData]:
        soup = BeautifulSoup(page_content.content, 'lxml')
        return soup.find_all('div', class_='col-md-12 col-sm-12 col-xs-12 col-lg-12')

    def get_apartment_title(self, apartment) -> Optional[str]:
        product_title = apartment.find('h3', class_='product-title')
        return product_title.find('a').text.strip()

    def get_apartment_link(self, apartment) -> Optional[str]:
        product_title = apartment.find('h3', class_='product-title')
        return product_title.find('a')['href']

    def get_rooms_number(self, apartment) -> Optional[str]:
        try:
            product_features = apartment.find('ul', class_='product-features')
            features_items = product_features.find_all('li', class_='col-p-1-3')
            rooms_div = features_items[1].find('div', class_='value-wrapper')
            return rooms_div.get_text().replace('Broj soba', '')[:3]
        except parser_exceptions.ApartmentRoomsNotFoundException:
            logging.warning(f"Rooms are not found for {product_features}")
            return None

    def get_apartment_city(self, apartment) -> Optional[str]:
        try:
            subtitle_places = apartment.find('ul', class_='subtitle-places')
            places_items = subtitle_places.find_all('li')
            return [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
        except parser_exceptions.ApartmentCityNotFoundException:
            logging.warning(f"City is not found for {subtitle_places}")
            return None

    def get_apartment_district(self, apartment) -> Optional[str]:
        try:
            subtitle_places = apartment.find('ul', class_='subtitle-places')
            places_items = subtitle_places.find_all('li')
            places = [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
            return places[2]
        except parser_exceptions.ApartmentDistrictNotFoundException:
            logging.warning(f"District is not found for {subtitle_places}")
            return None

    def get_apartment_price(self, apartment) -> Optional[str]:
        try:
            price_tag = apartment.find('div', class_='central-feature')
            return price_tag.find('span').text
        except parser_exceptions.ApartmentPriceNotFoundException:
            logging.warning(f"Price is not found for {price_tag}")
            return None
