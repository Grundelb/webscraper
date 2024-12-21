from telebot import types
from telebot.types import ReplyParameters
from apartmentsbot.apartment_manager import ApartmentManager, MyStates
import apartmentsbot.bot_messages


class BotHandler:

    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.apartment_manager = ApartmentManager()

    def start_help_message(self, message):
        self.bot.send_message(
            message.chat.id, apartmentsbot.bot_messages.MESSAGE_HELLO
        )

    def start_filter_get_city(self, message, state):
        state.delete()
        state.set(MyStates.city)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        cities = ["Novi Sad", "Beograd"]
        buttons = [types.KeyboardButton(city) for city in cities]
        keyboard.add(*buttons)
        self.bot.send_message(
            message.chat.id, apartmentsbot.bot_messages.PROMPT_ASK_CITY,
            reply_markup=keyboard
        )

    def price_get(self, message, state):
        state.set(MyStates.price)
        self.bot.send_message(message.chat.id,
                              apartmentsbot.bot_messages.PROMPT_ASK_MAX_PRICE,
                              reply_parameters=ReplyParameters(message_id=message.message_id))
        state.add_data(city=message.text)

    def area_get(self, message, state):
        state.set(MyStates.area)
        self.bot.send_message(message.chat.id,
                              apartmentsbot.bot_messages.PROMPT_ASK_MIN_AREA,
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
            apartmentsbot.bot_messages.PROMPT_ASK_ROOMS,
            reply_markup=keyboard, reply_parameters=ReplyParameters(message_id=message.message_id)
        )
        state.add_data(area=message.text)

    def filter_finish(self, message, state):
        state.set(MyStates.next_data)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("GET APARTMENTS")
        self.bot.send_message(
            message.chat.id,
            apartmentsbot.bot_messages.PROMPT_GET_APARTMENTS,
            reply_markup=keyboard, reply_parameters=ReplyParameters(message_id=message.message_id)
        )
        state.add_data(rooms=message.text)

    def get_apartments(self, message, state):
        with state.data() as data:
            city = data.get("city")
            price = int(data.get("price"))
            area = float(data.get("area"))
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
                    apartmentsbot.bot_messages.PROMPT_GET_MORE_APARTMENTS,
                    reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("GET MORE")
                )
            else:
                self.bot.send_message(message.chat.id, apartmentsbot.bot_messages.MESSAGE_NO_APARTMENTS,
                                      reply_parameters=ReplyParameters(message_id=message.message_id))
        else:
            self.bot.send_message(message.chat.id, apartmentsbot.bot_messages.MESSAGE_NO_APARTMENTS,
                                  reply_parameters=ReplyParameters(message_id=message.message_id))

    def any_state(self, message, state):
        state.delete()
        self.bot.send_message(
            message.chat.id,
            apartmentsbot.bot_messages.MESSAGE_CLEAR_STATES,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )
