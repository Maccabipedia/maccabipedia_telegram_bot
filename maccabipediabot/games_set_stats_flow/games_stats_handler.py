import logging
from pprint import pformat

from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

from maccabipediabot.games_set_stats_flow.menus_keyboards import create_top_players_games_stats_keyboard, create_games_stats_main_menu_keyboard, \
    create_players_streaks_games_stats_keyboard
from maccabipediabot.games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions, GamesStatsMainMenuOptions, PlayersStreaksStatsMenuOptions
from maccabipediabot.general_handlers import help_handler
from maccabipediabot.handlers_utils import send_typing_action
from maccabipediabot.maccabi_games import get_games_by_filters

logger = logging.getLogger(__name__)

show_stats, select_top_players_stats, select_players_streaks_stats = range(3)


def go_back_to_games_stats_main_menu(update, context):
    reply_keyboard = create_games_stats_main_menu_keyboard()

    # This is not the first time the user sees this menu, adapt the tet accordingly
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesStatsMainMenuOptions.AFTER_FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return show_stats


@send_typing_action
def games_stats_action(update, context):
    logger.info(f"New user for games stats: {update.effective_chat.username}")

    reply_keyboard = create_games_stats_main_menu_keyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesStatsMainMenuOptions.FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return show_stats


@send_typing_action
def show_players_streaks_stats_menu_action(update, context):
    reply_keyboard = create_players_streaks_games_stats_keyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text=PlayersStreaksStatsMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_players_streaks_stats


@send_typing_action
def show_summary_stats_action(update, context):
    games = get_games_by_filters(context.user_data)
    summary_stats = games.results.json_dict()

    context.bot.send_message(chat_id=update.effective_chat.id, text=summary_stats)

    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_top_players_stats_menu_action(update, context):
    reply_keyboard = create_top_players_games_stats_keyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text=TopPlayersStatsMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_top_players_stats


@send_typing_action
def show_players_unbeaten_streaks_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players_streaks.get_players_with_best_unbeaten_streak()

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"השחקנים עם רצף 'לא מנוצחים' הארוך ביותר:"
                                                                    f"\n{pformat(top)}")
    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_players_winning_streaks_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players_streaks.get_players_with_best_win_streak()

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"השחקנים עם רצף הנצחונות הארוך ביותר:"
                                                                    f"\n{pformat(top)}")
    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_top_scorers_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.best_scorers[0:10]

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"הכובשים המובילים: {pformat(top)}")

    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_top_assisters_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.best_assisters[0:10]

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"המבשלים המובילים: {pformat(top)}")

    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def show_most_played_action(update, context):
    games = get_games_by_filters(context.user_data)
    top = games.players.most_played[0:10]

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"השחקנים ששיקחו הכי הרבה: {pformat(top)}")

    return go_back_to_games_stats_main_menu(update, context)


@send_typing_action
def finished_to_show_games_stats_action(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"ביי!")

    return ConversationHandler.END


def create_games_stats_conversion_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("games_stats", games_stats_action)],
        states={
            show_stats: [
                CallbackQueryHandler(show_top_players_stats_menu_action, pattern=f"^{GamesStatsMainMenuOptions.TOP_PLAYERS_STATS}$"),
                CallbackQueryHandler(show_players_streaks_stats_menu_action, pattern=f"^{GamesStatsMainMenuOptions.PLAYERS_STREAKS_STATS}$"),
                CallbackQueryHandler(show_summary_stats_action, pattern=f"^{GamesStatsMainMenuOptions.SUMMARY_STATS}$"),
                CallbackQueryHandler(finished_to_show_games_stats_action, pattern=f"^{GamesStatsMainMenuOptions.FINISH}$")],

            select_top_players_stats: [
                CallbackQueryHandler(show_top_scorers_action, pattern=f"^{TopPlayersStatsMenuOptions.TOP_SCORERS}$"),
                CallbackQueryHandler(show_top_assisters_action, pattern=f"^{TopPlayersStatsMenuOptions.TOP_ASSISTERS}$"),
                CallbackQueryHandler(show_most_played_action, pattern=f"^{TopPlayersStatsMenuOptions.MOST_PLAYED}$")],

            select_players_streaks_stats: [
                CallbackQueryHandler(show_players_winning_streaks_action, pattern=f"^{PlayersStreaksStatsMenuOptions.WINNING_STREAK}$"),
                CallbackQueryHandler(show_players_unbeaten_streaks_action, pattern=f"^{PlayersStreaksStatsMenuOptions.UNBEATEN_STREAK}$")],

        },
        fallbacks=[CommandHandler('help', help_handler)]
    )
