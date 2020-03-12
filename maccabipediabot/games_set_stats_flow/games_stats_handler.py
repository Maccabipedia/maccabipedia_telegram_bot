import logging
from pprint import pformat

from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

from maccabipediabot.games_set_stats_flow.menus_keyboards import show_games_stats_main_menu
from maccabipediabot.games_set_stats_flow.menus_options import GamesStatsMainMenuOptions
from maccabipediabot.general_handlers import help_handler
from maccabipediabot.handlers_utils import send_typing_action
from maccabipediabot.maccabi_games import get_games_by_filters

logger = logging.getLogger(__name__)

show_stats = range(1)


def go_back_to_games_stats_main_menu(update, context):
    show_games_stats_main_menu(update, context)
    return show_stats


@send_typing_action
def games_stats_action(update, context):
    logger.info(f"New user for games stats: {update.effective_chat.username}")

    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_top_scorers_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.best_scorers[0:10]

    logger.info(top)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"הכובשים המובילים: {pformat(top)}")

    go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_top_assisters_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.best_assisters[0:10]

    logger.info(top)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"המבשלים המובילים: {pformat(top)}")

    go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_most_played_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.most_played[0:10]

    logger.info(top)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"השחקנים ששיקחו הכי הרבה: {pformat(top)}")

    go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def finished_to_show_games_stats_action(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"ביי!")

    return ConversationHandler.END


def create_games_stats_conversion_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("games_stats", games_stats_action)],
        states={
            show_stats: [CallbackQueryHandler(show_top_scorers_action, pattern=f"^{GamesStatsMainMenuOptions.TOP_SCORERS}$"),
                         CallbackQueryHandler(show_top_assisters_action, pattern=f"^{GamesStatsMainMenuOptions.TOP_ASSISTERS}$"),
                         CallbackQueryHandler(show_most_played_action, pattern=f"^{GamesStatsMainMenuOptions.MOST_PLAYED}$"),
                         CallbackQueryHandler(finished_to_show_games_stats_action, pattern=f"^{GamesStatsMainMenuOptions.FINISH}$")],

        },
        fallbacks=[CommandHandler('help', help_handler)]
    )
