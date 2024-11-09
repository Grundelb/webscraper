from bs4 import BeautifulSoup
from parser.abstract_scraper import AbstractScraper, ApartmentPageData
from parser.parser_exceptions import ApartmentParseError
from typing import Optional
from utility import suppress


class HalooglasiScraper(AbstractScraper):
    BASE_URL = 'https://www.halooglasi.com/nekretnine/izdavanje-stanova'

    def fetch_apartment_listings(self, page_content) -> list[ApartmentPageData]:
        soup = BeautifulSoup(page_content.content, 'lxml')
        return soup.find_all('div', class_='col-md-12 col-sm-12 col-xs-12 col-lg-12')

    @suppress(ApartmentParseError, "Title not found")
    def get_apartment_title(self, apartment) -> Optional[str]:
        product_title = apartment.find('h3', class_='product-title')
        if product_title:
            return product_title.find('a').text.strip()
        else:
            raise ApartmentParseError(f"Title is not found for {product_title}")

    @suppress(ApartmentParseError, "Link not found")
    def get_apartment_link(self, apartment) -> Optional[str]:
        apartment_link = apartment.find('h3', class_='product-title')
        if apartment_link:
            return self.BASE_URL + apartment_link.find('a')['href']
        else:
            raise ApartmentParseError(f"Link is not found for {apartment_link}")

    @suppress(ApartmentParseError, "Rooms not found")
    def get_rooms_number(self, apartment) -> Optional[str]:
        product_features = apartment.find('ul', class_='product-features')
        features_items = product_features.find_all('li', class_='col-p-1-3')
        rooms_div = features_items[1].find('div', class_='value-wrapper')
        if rooms_div:
            return rooms_div.get_text().replace('Broj soba', '')[:3]
        else:
            raise ApartmentParseError(f"Rooms are not found for {product_features}")

    @suppress(ApartmentParseError, "City not found")
    def get_apartment_city(self, apartment) -> Optional[str]:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        places_items = subtitle_places.find_all('li')
        if places_items:
            return [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)][0]
        else:
            raise ApartmentParseError(f"City is not found for {subtitle_places}")

    @suppress(ApartmentParseError, "District not found")
    def get_apartment_district(self, apartment) -> Optional[str]:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        places_items = subtitle_places.find_all('li')
        places = [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
        if places:
            return places[2]
        else:
            raise ApartmentParseError(f"District is not found for {subtitle_places}")

    @suppress(ApartmentParseError, "Price not found")
    def get_apartment_price(self, apartment) -> Optional[str]:
        price_tag = apartment.find('div', class_='central-feature')
        if price_tag:
            return price_tag.find('span').text
        else:
            raise ApartmentParseError(f"Price is not found for {price_tag}")
