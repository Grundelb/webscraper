from abc import ABC, abstractmethod
from parser.apartment import Apartment


class BaseScraper(ABC):

    def __init__(self):
        self.apartments_data = []

    @abstractmethod
    def fetch_apartment_listings(self, page_content) -> list[str]:
        pass

    @abstractmethod
    def get_apartment_title(self, apartment) -> str:
        pass

    @abstractmethod
    def get_apartment_link(self, apartment) -> str:
        pass

    @abstractmethod
    def get_rooms_number(self, apartment) -> str:
        pass

    @abstractmethod
    def get_apartment_city(self, apartment) -> str:
        pass

    @abstractmethod
    def get_apartment_district(self, apartment) -> str:
        pass

    @abstractmethod
    def get_apartment_price(self, apartment) -> str:
        pass

    def parse_page(self, apartment_listings) -> int:
        """
        Func to find apartments on the page
        If the title or link is missing, skip this listing
        :param apartment_listings: list of apartments
        :return: The number of listings on the page is returned,
        and it is used to determine if the page is the last one.
        """
        page_size = []
        for index, apartment in enumerate(apartment_listings):
            title = self.get_apartment_title(apartment)
            link_to_apartment = self.get_apartment_link(apartment)

            if not title or not link_to_apartment:
                continue

            city = self.get_apartment_city(apartment)
            district = self.get_apartment_district(apartment)
            rooms = self.get_rooms_number(apartment)
            price = self.get_apartment_price(apartment)

            apartment_obj = Apartment(title, link_to_apartment, rooms, city, district, price)
            self.apartments_data.append(apartment_obj)
            page_size.append(index)

        return len(page_size)
