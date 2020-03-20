import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from maccabipediabot.create_games_set_flow.games_set_handler import create_games_set_conversion_handler
from maccabipediabot.games_set_stats_flow.games_stats_handler import create_games_stats_conversion_handler
from maccabipediabot.general_handlers import help_handler, start_handler, shirt_number_handler, song_handler, donation_handler, \
    unknown_message_handler, error_callback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def load_env_file():
    logger.info("Loading env variable from .env if exists")
    load_dotenv(verbose=True)


def register_telegram_bot():
    logger.info("Starting registering the bot!")
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = Updater(token=bot_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("shirt_number", shirt_number_handler))
    updater.dispatcher.add_handler(CommandHandler("song", song_handler))
    updater.dispatcher.add_handler(CommandHandler("donate", donation_handler))

    updater.dispatcher.add_handler(create_games_set_conversion_handler())
    updater.dispatcher.add_handler(create_games_stats_conversion_handler())

    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_message_handler))
    updater.dispatcher.add_error_handler(error_callback)
    logger.info("Starting to run the bot!")
    updater.start_polling(clean=True)


if __name__ == "__main__":
    load_env_file()
    register_telegram_bot()
