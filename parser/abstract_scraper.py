import logging
from abc import ABC, abstractmethod
from parser.apartment import Apartment
from typing import Any, Optional

ApartmentPageData = Any


class AbstractScraper(ABC):

    @abstractmethod
    def fetch_apartment_listings(self, page_content) -> list[ApartmentPageData]:
        pass

    @abstractmethod
    def get_apartment_title(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    @abstractmethod
    def get_apartment_link(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    @abstractmethod
    def get_rooms_number(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    @abstractmethod
    def get_apartment_city(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    @abstractmethod
    def get_apartment_district(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    @abstractmethod
    def get_apartment_price(self, apartment: ApartmentPageData) -> Optional[str]:
        pass

    def parse_page(self, apartment_listings: ApartmentPageData) -> list[Apartment]:
        """
        Func to find apartments on the page
        If the title or link is missing, skip this listing
        :param apartment_listings: list of apartments
        :return: The number of listings on the page is returned,
        and it is used to determine if the page is the last one.
        """
        apartments_data = []
        for apartment in apartment_listings:
            title = self.get_apartment_title(apartment)
            link_to_apartment = self.get_apartment_link(apartment)

            if not title or not link_to_apartment:
                logging.error(f"Skipping apartment due to missing critical data: {title}, {link_to_apartment}")
                continue

            city = self.get_apartment_city(apartment)
            district = self.get_apartment_district(apartment)
            rooms = self.get_rooms_number(apartment)
            price = self.get_apartment_price(apartment)

            apartment_obj = Apartment(title, link_to_apartment, rooms, city, district, price)
            apartments_data.append(apartment_obj)

        return apartments_data
