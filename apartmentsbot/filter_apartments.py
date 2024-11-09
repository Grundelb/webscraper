from utility import get_all_apartments


class FilterApartments:

    def _prepare_data_for_filtering(self, apartments):
        prepared_apartments = []
        for apartment in apartments:
            try:
                price = int(apartment['price'].replace('\u00a0', '').replace('€', '').replace('.', '').strip())

                rooms = int(apartment['rooms'][0])

                prepared_apartment = {
                    'title': apartment['title'],
                    'link': apartment['link'],
                    'rooms': rooms,
                    'city': apartment['city'],
                    'district': apartment['district'],
                    'price': price
                }
                prepared_apartments.append(prepared_apartment)
            except (ValueError, TypeError, KeyError) as e:
                print(f"Ошибка при обработке квартиры '{apartment['title']}': {e}")
                continue

        return prepared_apartments

    def _filter_apartments(self, filters, apartments):
        return list(filter(lambda apartment: apartment['city'] == filters['city']
                                             and apartment['rooms'] == filters['rooms']
                                             and filters['min_price'] <= apartment['price'] <= filters['max_price'],
                           apartments))

    def _lazy_load_apartments(self, apartments, batch_size=10):
        for i in range(0, len(apartments), batch_size):
            yield apartments[i:i + batch_size]

    def execute_filter(self, filters):
        apartments = get_all_apartments()
        cleared_apartments = self._prepare_data_for_filtering(apartments)
        filtered_apartments = self._filter_apartments(cleared_apartments, filters)
        return self._lazy_load_apartments(filtered_apartments)



