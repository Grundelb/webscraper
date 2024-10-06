from bs4 import BeautifulSoup
from src.apartment import Apartment


class Scraper:
    data = []

    def get_all_apartments_on_the_page(self, response) -> list:
        soup = BeautifulSoup(response.content, 'lxml')
        listings = soup.find_all('div', class_='row')
        return listings

    def parse_raw_halooglasi(self, apartments) -> int:
        """
        Func to find of apartments on the page
        :param apartments: list of apartments
        :return: count of apartments
        """
        page_size = []
        for index, apartment in enumerate(apartments):

            product_title = apartment.find('h3', class_='product-title')
            title = None
            link_to_apartment = None
            if product_title:
                page_size.append(index)
                title = product_title.find('a').text.strip()
                link_to_apartment = product_title.find('a')['href']

            product_features = apartment.find('ul', class_='product-features')
            rooms = None
            if product_features:
                features_items = product_features.find_all('li', class_='col-p-1-3')
                if len(features_items) >= 2:
                    rooms_div = features_items[1].find('div', class_='value-wrapper')
                    if rooms_div:
                        rooms = rooms_div.get_text().replace('Broj soba', '').strip()

            subtitle_places = apartment.find('ul', class_='subtitle-places')
            city = None
            district = None
            if subtitle_places:
                places_items = subtitle_places.find_all('li')
                places = [item.get_text(strip=True) for item in places_items if item.get_text(strip=True)]
                if len(places) >= 3:
                    city = places[0]
                    district = places[2]
                elif len(places) >= 2:
                    city = places[0]
                    district = places[1]
            price_tag = apartment.find('div', class_='central-feature')
            price = None
            if price_tag:
                price = price_tag.find('span').text

            if title and link_to_apartment and city and district:
                apartment_obj = Apartment(title, link_to_apartment, rooms, city, district, price)
                self.data.append(apartment_obj)

        return len(page_size)
