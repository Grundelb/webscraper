from telebot.states import State, StatesGroup
from telebot.storage import StateMemoryStorage
from apartmentsbot.filter_apartments import FilterApartments


state_storage = StateMemoryStorage()

class MyStates(StatesGroup):
    city = State()
    min_price = State()
    max_price = State()
    rooms = State()
    next_data = State()

class ApartmentManager:
    def __init__(self):
        self.apartments = []
        self.index = 0

    def load_apartments(self, city, min_price, max_price, rooms):
        apartment_filter = FilterApartments()
        self.apartments = apartment_filter.execute_filter(city, min_price, max_price, rooms)
        self.index = 0

    def get_next_batch(self, batch_size=5):
        start = self.index
        end = start + batch_size
        self.index = end
        return self.apartments[start:end]

    def has_more(self):
        return self.index < len(self.apartments)
