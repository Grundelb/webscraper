from telebot.states.sync.middleware import StateMiddleware
from telebot import custom_filters, types
from telebot.states.sync.context import StateContext
from apartmentsbot.apartment_manager import state_storage, MyStates
from apartmentsbot.bot_handler import BotHandler
from utility import load_config
import apartmentsbot.bot_messages
import logging
import telebot

logging.basicConfig(level=logging.INFO, filename="apartment_bot.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

config = load_config()
API_TOKEN = config["bot"]["API_TOKEN"]

bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage, use_class_middlewares=True)
bot_handler = BotHandler(bot)


@bot.message_handler(commands=["start", "help"])
def start_help(message: types.Message):
    bot_handler.start_help_message(message)


@bot.message_handler(commands=["filter"])
def start_filter(message: types.Message, state: StateContext):
    bot_handler.start_filter_get_city(message, state)


@bot.message_handler(state=MyStates.city, text=["Novi Sad", "Beograd"])
def price_get(message: types.Message, state: StateContext):
    bot_handler.price_get(message, state)


@bot.message_handler(state=MyStates.price, is_digit=True)
def area_get(message: types.Message, state: StateContext):
    bot_handler.area_get(message, state)


@bot.message_handler(state=MyStates.area, is_digit=True)
def rooms_number_get(message: types.Message, state: StateContext):
    bot_handler.rooms_number_get(message, state)


@bot.message_handler(state=MyStates.rooms, text=["1", "2", "3", "4"])
def filter_finish(message: types.Message, state: StateContext):
    bot_handler.filter_finish(message, state)


@bot.message_handler(state=MyStates.next_data, text="GET APARTMENTS")
def get_apartments(message: types.Message, state: StateContext):
    bot_handler.get_apartments(message, state)


@bot.message_handler(text="GET MORE")
def get_more_apartments(message: types.Message):
    bot_handler.get_more_apartments(message)


@bot.message_handler(state=[MyStates.area, MyStates.price], is_digit=False)
def price_incorrect(message: types.Message):
    bot.send_message(
        message.chat.id, apartmentsbot.bot_messages.ERROR_INVALID_NUMBER
    )


@bot.message_handler(state="*", commands=["cancel"])
def clear_state(message: types.Message, state: StateContext):
    bot_handler.any_state(message, state)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
