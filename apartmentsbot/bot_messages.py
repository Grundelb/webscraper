class BotMessages:
    MESSAGE_HELLO = (
        "Hello! I'm a bot for finding apartments in Belgrade or Novi Sad.\n\n"
        "To start your search, enter the command /filter and answer the questions "
        "so I can find the best options for you!"
    )
    MESSAGE_NO_APARTMENTS = "No more apartments available."
    MESSAGE_CLEAR_STATES = "Your information has been cleared. Type /start to begin again."

    PROMPT_ASK_CITY = "What is your city? Choose from the options below."
    PROMPT_ASK_MAX_PRICE = "What is the maximum price you are willing to pay for an apartment (in EUR)?"
    PROMPT_ASK_MIN_AREA = "What is the minimum apartment size you are looking for (in square meters)?"
    PROMPT_ASK_ROOMS = "How many rooms do you looking for? Choose from the options below."
    PROMPT_GET_APARTMENTS = "Click on 'GET APARTMENTS'"
    PROMPT_GET_MORE_APARTMENTS = "Click on 'GET MORE' to see the next batch."

    ERROR_INVALID_NUMBER = "Please enter a valid number."
