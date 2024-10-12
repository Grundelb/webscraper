from parser.network_connector import NetworkConnector
from parser.scraper_halooglasi import HalooglasiScraper


def main():
    page_number = 1
    scraper = HalooglasiScraper()
    connector = NetworkConnector(HalooglasiScraper.BASE_URL)

    while True:
        response = connector.load_listing_page(page_number)
        new_data = scraper.fetch_apartment_listings(response)

        if not new_data:
            break

        fetch_data = scraper.parse_page(new_data)

        if fetch_data >= 20:
            page_number += 1
        else:
            break

    return scraper.apartments_data


if __name__ == "__main__":
    main()
