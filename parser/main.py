from parser.network_connector import NetworkConnector
from parser.scraper_halooglasi import HalooglasiScraper
from parser.utility import save_list_of_apartments
from dataclasses import asdict


def main():
    page_number = 1
    scraper = HalooglasiScraper()
    connector = NetworkConnector(HalooglasiScraper.BASE_URL)
    apartment_list = []
    while True:
        response = connector.load_listing_page(page_number)
        new_data = scraper.fetch_apartment_listings(response)

        if not new_data:
            break

        fetch_data = scraper.parse_page(new_data)
        for apartment in fetch_data:
            apartment_list.append(asdict(apartment))

        if len(fetch_data) >= 20:
            page_number += 1
        else:
            break

    save_list_of_apartments(apartment_list, "apartment_data.json")


if __name__ == "__main__":
    main()
