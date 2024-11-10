import logging
import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.states.sync.middleware import StateMiddleware
from telebot.types import ReplyParameters
from apartmentsbot.filter_apartments import FilterApartments

logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

API_TOKEN = '8114799053:AAFQUn565x0j-5mZatTNDCvDIjwUOtd2Vd0'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage, use_class_middlewares=True)


class MyStates(StatesGroup):
    city = State()
    min_price = State()
    max_price = State()
    rooms = State()
    next_data = State()


@bot.message_handler(commands=["start", "help"])
def start_help_message(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Hello! I'm a bot for finding apartments in Belgrade or Novi Sad.\n"
        "To start your search, enter the command /filter and answer the questions "
        "so I can find the best options for you!"
    )


@bot.message_handler(commands=["filter"])
def start_filter_get_city(message: types.Message, state: StateContext):
    state.delete()
    state.set(MyStates.city)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    cities = ["Novi Sad", "Belgrade"]
    buttons = [types.KeyboardButton(city) for city in cities]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "What is your city? Choose from the options below.",
        reply_markup=keyboard,
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )


# Cancel command handler
@bot.message_handler(state="*", commands=["cancel"])
def any_state(message: types.Message, state: StateContext):
    state.delete()
    bot.send_message(
        message.chat.id,
        "Your information has been cleared. Type /start to begin again.",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )


@bot.message_handler(state=MyStates.city, text=["Novi Sad", "Belgrade"])
def min_price_get(message: types.Message, state: StateContext):
    state.set(MyStates.min_price)
    bot.send_message(
        message.chat.id, "What is min price (EUR)?",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    state.add_data(city=message.text)


@bot.message_handler(state=MyStates.min_price, is_digit=True)
def max_price_get(message: types.Message, state: StateContext):
    state.set(MyStates.max_price)
    bot.send_message(
        message.chat.id, "What is max price (EUR)?",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    state.add_data(min_price=message.text)


@bot.message_handler(state=MyStates.max_price, is_digit=True)
def rooms_number_get(message: types.Message, state: StateContext):
    state.set(MyStates.rooms)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rooms_number = ["1", "2", "3", "4"]
    buttons = [types.KeyboardButton(room) for room in rooms_number]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "How many rooms do you looking for? Choose from the options below.",
        reply_markup=keyboard,
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    state.add_data(max_price=message.text)


@bot.message_handler(
    state=MyStates.rooms, text=["1", "2", "3", "4"]
)
def filter_finish(message: types.Message, state: StateContext):
    state.set(MyStates.next_data)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("GET APARTMENTS")

    bot.send_message(
        message.chat.id,
        "Click on GET APARTMENTS",
        reply_markup=keyboard,
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    state.add_data(rooms=message.text)


@bot.message_handler(state=MyStates.next_data)
def send_apartments(message: types.Message, state: StateContext):
    with state.data() as data:
        city = data.get("city")
        min_price = int(data.get("min_price"))
        max_price = int(data.get("max_price"))
        rooms = int(data.get("rooms"))

    logging.info(f"Filters set to: city={city}, min_price={min_price}, max_price={max_price}, rooms={rooms}")
    apartment_batches = FilterApartments.execute_filter(city, min_price, max_price, rooms)

    for batch in apartment_batches:
        for apartment in batch:
            bot.send_message(
                message.chat.id,
                f"Title: {apartment['title']}\n"
                f"City: {apartment['city']}\n"
                f"District: {apartment['district']}\n"
                f"Price: {apartment['price']} EUR\n"
                f"Rooms: {apartment['rooms']}\n"
                f"Link: {apartment['link']}"
            )
        # Wait for user to request the next batch
        bot.send_message(
            message.chat.id,
            "Type 'GET MORE' to see the next batch.",
            reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("GET MORE")
        )
        break


@bot.message_handler(state=[MyStates.max_price, MyStates.min_price], is_digit=False)
def price_incorrect(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Please enter a valid number.",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
