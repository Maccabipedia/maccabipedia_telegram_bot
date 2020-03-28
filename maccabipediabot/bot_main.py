# Hacks for heroku
import matplotlib

matplotlib.use('Agg')

import logging
import os

from maccabipediabot.loggers import initialize_loggers

# This should stay before the rest of this package imports to enable logging to file
initialize_loggers()

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from maccabipediabot.create_games_set_flow.games_set_handler import create_games_set_conversion_handler
from maccabipediabot.games_set_stats_flow.games_stats_handler import create_games_stats_conversion_handler
from maccabipediabot.general_handlers import help_handler, start_handler, unknown_message_handler, error_callback
from maccabipediabot.simple_flows.player_details_flow import create_player_conversation_handler
from maccabipediabot.simple_flows.donation_flow import create_donation_handlers
from maccabipediabot.simple_flows.season_details_flow import create_season_conversation_handler
from maccabipediabot.simple_flows.song_details_flow import create_song_conversation_handler
from maccabipediabot.simple_flows.uniforms_flow import create_uniforms_conversation_handler

logger = logging.getLogger("maccabipediabot")


def load_env_file():
    logger.info("Loading env variable from .env if exists")
    load_dotenv(verbose=True)


def register_telegram_bot():
    """
    Some general comments:
    Because we used ReplyKeyboard (We are replacing the user keyboard with our buttons),
    We have to add and remove this keyboard from time to time within out interaction with the user.

    When the user chose something from the main keyboard we remove the ReplyKeyboard,
    When the user finish an sub-operation (that was chosen from the ReplyKeyboard) we re-add the ReplyKeyboard.

    Moreover, we support two options to start some handlers:
    1) Start by command, like "/give_me_stats"
    2) Start by message, like "אני רוצה לראות סטטיסטיקות"
    Both will point to same behaviour.

    We support in the more "simple" conversation handlers (everything exclude "games filtering" and "games stats")
    to go back to the main menu in the middle of the conversation.
    In order to do that we replace the ReplyKeyboard to one with just "Go back" button (At the start of each relevant conversation).
    """
    logger.info("Starting registering the bot!")
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token=bot_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))

    donation_command_handler, donation_message_handler = create_donation_handlers()
    updater.dispatcher.add_handler(donation_command_handler)
    updater.dispatcher.add_handler(donation_message_handler)

    updater.dispatcher.add_handler(create_season_conversation_handler())
    updater.dispatcher.add_handler(create_song_conversation_handler())
    updater.dispatcher.add_handler(create_player_conversation_handler())
    updater.dispatcher.add_handler(create_uniforms_conversation_handler())

    updater.dispatcher.add_handler(create_games_set_conversion_handler())
    updater.dispatcher.add_handler(create_games_stats_conversion_handler())

    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_message_handler))
    updater.dispatcher.add_error_handler(error_callback)

    # updater.dispatcher.add_handler(CommandHandler("shirt_number", shirt_number_handler)) This command is not good enough for now

    logger.info("Starting to run the bot!")
    updater.start_polling(clean=True)


if __name__ == "__main__":
    load_env_file()
    register_telegram_bot()
