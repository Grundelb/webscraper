from telebot import types
from telebot.types import ReplyParameters
from apartmentsbot.apartment_manager import ApartmentManager, MyStates


class BotHandler:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.apartment_manager = ApartmentManager()

    def start_help_message(self, message):
        self.bot.send_message(
            message.chat.id,
            "Hello! I'm a bot for finding apartments in Belgrade or Novi Sad.\n"
            "To start your search, enter the command /filter and answer the questions "
            "so I can find the best options for you!"
        )

    def start_filter_get_city(self, message, state):
        state.delete()
        state.set(MyStates.city)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        cities = ["Novi Sad", "Beograd"]
        buttons = [types.KeyboardButton(city) for city in cities]
        keyboard.add(*buttons)
        self.bot.send_message(
            message.chat.id,
            "What is your city? Choose from the options below.",
            reply_markup=keyboard
        )

    def price_get(self, message, state):
        state.set(MyStates.price)
        self.bot.send_message(message.chat.id,
                              "What is the maximum price you are willing to pay for an apartment (in EUR)?",
                              reply_parameters=ReplyParameters(message_id=message.message_id))
        state.add_data(city=message.text)

    def area_get(self, message, state):
        state.set(MyStates.area)
        self.bot.send_message(message.chat.id,
                              "What is the minimum apartment size you are looking for (in square meters)?",
                              reply_parameters=ReplyParameters(message_id=message.message_id))
        state.add_data(price=message.text)

    def rooms_number_get(self, message, state):
        state.set(MyStates.rooms)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        rooms_number = ["1", "2", "3", "4"]
        buttons = [types.KeyboardButton(room) for room in rooms_number]
        keyboard.add(*buttons)
        self.bot.send_message(
            message.chat.id,
            "How many rooms do you looking for? Choose from the options below.",
            reply_markup=keyboard, reply_parameters=ReplyParameters(message_id=message.message_id)
        )
        state.add_data(area=message.text)

    def filter_finish(self, message, state):
        state.set(MyStates.next_data)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("GET APARTMENTS")
        self.bot.send_message(
            message.chat.id,
            "Click on GET APARTMENTS",
            reply_markup=keyboard, reply_parameters=ReplyParameters(message_id=message.message_id)
        )
        state.add_data(rooms=message.text)

    def get_apartments(self, message, state):
        with state.data() as data:
            city = data.get("city")
            price = int(data.get("price"))
            area = int(data.get("area"))
            rooms = int(data.get("rooms"))

        self.apartment_manager.load_apartments(city, area, price, rooms)
        self.send_apartment_batch(message)

    def get_more_apartments(self, message):
        self.send_apartment_batch(message)

    def send_apartment_batch(self, message):
        batch = self.apartment_manager.get_next_batch()
        if batch:
            for apartment in batch:
                self.bot.send_message(
                    message.chat.id,
                    f"Title: {apartment['title']}\n"
                    f"Date: {apartment['date']}\n"
                    f"City: {apartment['city']}\n"
                    f"District: {apartment['district']}\n"
                    f"Price: {apartment['price']} EUR\n"
                    f"Rooms: {apartment['rooms']}\n"
                    f"Area: {apartment['area']}\n"
                    f"Link: {apartment['link']}"
                )
            if self.apartment_manager.has_more():
                self.bot.send_message(
                    message.chat.id,
                    "Type 'GET MORE' to see the next batch.",
                    reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("GET MORE")
                )
            else:
                self.bot.send_message(message.chat.id, "No more apartments available.",
                                      reply_parameters=ReplyParameters(message_id=message.message_id))
        else:
            self.bot.send_message(message.chat.id, "No more apartments available.",
                                  reply_parameters=ReplyParameters(message_id=message.message_id))

    def any_state(self, message, state):
        state.delete()
        self.bot.send_message(
            message.chat.id,
            "Your information has been cleared. Type /start to begin again.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )
