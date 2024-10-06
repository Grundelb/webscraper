from src.network_connector import NetworkConnector
from src.scraper import Scraper


class Main:

    @staticmethod
    def main():
        number = 1
        connector = NetworkConnector()
        scraper = Scraper()

        while True:
            response = connector.get_data(number)
            new_data = scraper.get_all_apartments_on_the_page(response)

            if not new_data:
                break

            fetch_data = scraper.parse_raw_halooglasi(new_data)

            if fetch_data >= 20:
                number += 1
            else:
                break

        for items in scraper.data:
            print(items)


if __name__ == "__main__":
    Main.main()
