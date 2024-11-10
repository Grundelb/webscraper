from parser.network_connector import NetworkConnector
from parser.scraper_halooglasi import HalooglasiScraper
from utility import save_list_of_apartments
from dataclasses import asdict
import logging


def execute_parser(city_path):
    logging.basicConfig(level=logging.INFO, filename="scraper_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    page_number = 1
    scraper = HalooglasiScraper()
    connector = NetworkConnector(HalooglasiScraper.SEARCH_URL)
    apartment_list = []
    logging.info("Execution started")
    logging.info(f"URL: {HalooglasiScraper.SEARCH_URL}")
    while True:
        logging.info(f"Page number: {page_number}\n")
        response = connector.load_listing_page(page_number, city_path)
        new_data = scraper.fetch_apartment_listings(response)

        if not new_data:
            break

        fetch_data = scraper.parse_page(new_data)
        logging.info(f"Apartments data was fetched successfully: {fetch_data}\n")
        for apartment in fetch_data:
            apartment_list.append(asdict(apartment))

        if len(fetch_data) >= 20:
            page_number += 1
        else:
            break

    save_list_of_apartments(apartment_list)
    logging.info(f"Apartments added: {len(apartment_list)}")
    logging.info("Execution completed")


execute_parser('/novi-sad')
execute_parser('/beograd')
