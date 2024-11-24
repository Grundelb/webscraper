from bs4 import BeautifulSoup
from parser.abstract_scraper import AbstractScraper, ApartmentPageData
from parser.parser_exceptions import ApartmentParseError
from typing import Optional
from utility import suppress


class HalooglasiScraper(AbstractScraper):
    SEARCH_URL = 'https://www.halooglasi.com/nekretnine/izdavanje-stanova'
    BASE_URL = 'https://www.halooglasi.com'

    def fetch_apartment_listings(self, page_content) -> list[ApartmentPageData]:
        soup = BeautifulSoup(page_content.content, 'lxml')
        return soup.find_all('div', class_='col-md-12 col-sm-12 col-xs-12 col-lg-12')

    @suppress(ApartmentParseError, "Title not found")
    def get_apartment_title(self, apartment) -> Optional[str]:
        product_title = apartment.find('h3', class_='product-title')
        if product_title:
            return product_title.find('a').get_text(strip=True)
        raise ApartmentParseError(f"Title is not found for {product_title}")

    @suppress(ApartmentParseError, "Link not found")
    def get_apartment_link(self, apartment) -> Optional[str]:
        apartment_link = apartment.find('h3', class_='product-title')
        if apartment_link:
            return self.BASE_URL + apartment_link.find('a')['href']
        raise ApartmentParseError(f"Link is not found for {apartment_link}")

    @suppress(ApartmentParseError, "Rooms not found")
    def get_rooms_number(self, apartment) -> Optional[int]:
        product_features = apartment.find('ul', class_='product-features')
        features_items = product_features.find_all('li', class_='col-p-1-3')
        rooms_div = features_items[1].find('div', class_='value-wrapper')
        if rooms_div:
            # Index 0 trims the string containing the number of rooms, leaving only the number (the first digit).
            return int(rooms_div.get_text(strip=True).replace('Broj soba', '')[0])
        raise ApartmentParseError(f"Rooms are not found for {product_features}")

    @suppress(ApartmentParseError, "City not found")
    def get_apartment_city(self, apartment) -> Optional[str]:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        places_items = subtitle_places.find_all('li')
        if places_items:
            # Index 0 corresponds to the city in the subtitle_places list.
            return [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)][0]
        raise ApartmentParseError(f"City is not found for {subtitle_places}")

    @suppress(ApartmentParseError, "District not found")
    def get_apartment_district(self, apartment) -> Optional[str]:
        subtitle_places = apartment.find('ul', class_='subtitle-places')
        places_items = subtitle_places.find_all('li')
        if places_items:
            # Index 2 corresponds to the district in the subtitle_places list.
            return [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)][2]
        raise ApartmentParseError(f"District is not found for {subtitle_places}")

    @suppress(ApartmentParseError, "Price not found")
    def get_apartment_price(self, apartment) -> Optional[int]:
        price_tag = apartment.find('div', class_='central-feature')
        if price_tag:
            return int(
                price_tag.find('span').get_text(strip=True).replace('\u00a0', '').replace('€', '').replace('.', ''))
        raise ApartmentParseError(f"Price is not found for {price_tag}")

    @suppress(ApartmentParseError, "Failed to get apartment area")
    def get_apartment_area(self, apartment) -> Optional[int]:
        product_features = apartment.find('ul', class_='product-features')
        features_items = product_features.find_all('li', class_='col-p-1-3')
        area_div = features_items[0].find('div', class_='value-wrapper')
        if area_div:
            return float(area_div.get_text(strip=True).replace('\xa0m2Kvadratura', '').replace(',', '.'))
        raise ApartmentParseError(f"Apartment area not found for {area_div}")

    @suppress(ApartmentParseError, "Failed to get apartment posting date")
    def get_apartment_date(self, apartment) -> str:
        date_tag = apartment.find('span', class_='publish-date')
        if date_tag:
            # Trimming the last char in the string: `.`
            return date_tag.get_text(strip=True)[:-1]
        raise ApartmentParseError(f"Posting date not found for {date_tag}")
