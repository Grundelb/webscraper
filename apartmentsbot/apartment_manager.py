from telebot.states import State, StatesGroup
from telebot.storage import StateMemoryStorage
from utility import get_all_apartments
from parser.apartment import Apartment

state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    city = State()
    price = State()
    area = State()
    rooms = State()
    next_data = State()


class ApartmentManager:
    def __init__(self):
        self.apartments = []
        self.index = 0

    def load_apartments(self, city: str, area: int, max_price: int, rooms: int) -> None:
        self.apartments = self.execute_filter(city, area, max_price, rooms)
        self.index = 0

    def get_next_batch(self, batch_size=5) -> list[Apartment]:
        start = self.index
        end = start + batch_size
        self.index = end
        return self.apartments[start:end]

    def has_more(self) -> bool:
        return self.index < len(self.apartments)

    def _filter_apartments(self, city: State, area: State, max_price: State, rooms: State,
                           apartments: list[Apartment]) -> list[Apartment]:
        return list(filter(lambda apartment: apartment['city'] == city
                                             and apartment['rooms'] == rooms
                                             and apartment['price'] <= max_price
                                             and apartment['area'] >= area,
                           apartments))

    def execute_filter(self, city: State, area: State, max_price: State, rooms: State) -> list[Apartment]:
        apartments = get_all_apartments()
        filtered_apartments = self._filter_apartments(city, area, max_price, rooms, apartments)
        return filtered_apartments
