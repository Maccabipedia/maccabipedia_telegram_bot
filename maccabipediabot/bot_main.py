# Hacks for heroku
import matplotlib
matplotlib.use('Agg')

import logging
import os

from maccabipediabot.loggers import initialize_loggers
from maccabipediabot.maccabi_games import download_maccabipedia_games_for_heroku

# This should stay before the rest of this package imports to enable logging to file
initialize_loggers()

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from maccabipediabot.create_games_set_flow.games_set_handler import create_games_set_conversion_handler
from maccabipediabot.games_set_stats_flow.games_stats_handler import create_games_stats_conversion_handler
from maccabipediabot.general_handlers import help_handler, start_handler, song_handler, \
    donation_handler, profile_handler, season_details_handler, unknown_message_handler, error_callback

logger = logging.getLogger("maccabipediabot")


def load_env_file():
    logger.info("Loading env variable from .env if exists")
    load_dotenv(verbose=True)


def register_telegram_bot():
    logger.info("Starting registering the bot!")
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token=bot_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    # updater.dispatcher.add_handler(CommandHandler("shirt_number", shirt_number_handler)) This command is not good enough for now
    updater.dispatcher.add_handler(CommandHandler("profile", profile_handler))
    updater.dispatcher.add_handler(CommandHandler("song", song_handler))
    updater.dispatcher.add_handler(CommandHandler("season", season_details_handler))
    updater.dispatcher.add_handler(CommandHandler("donate", donation_handler))

    updater.dispatcher.add_handler(create_games_set_conversion_handler())
    updater.dispatcher.add_handler(create_games_stats_conversion_handler())

    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_message_handler))
    updater.dispatcher.add_error_handler(error_callback)
    logger.info("Starting to run the bot!")
    updater.start_polling(clean=True)


if __name__ == "__main__":
    download_maccabipedia_games_for_heroku()
    load_env_file()
    register_telegram_bot()
