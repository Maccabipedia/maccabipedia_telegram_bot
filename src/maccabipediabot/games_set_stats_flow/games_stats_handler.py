import logging

from telegram import ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY, set_default_filters_for_current_user
from maccabipediabot.games_set_stats_flow.common_menu import go_back_to_games_stats_main_menu
from maccabipediabot.games_set_stats_flow.games_stats_conversation_handler_states import show_stats, \
    select_more_stats_or_finish, \
    select_players_streaks_stats, select_top_players_stats, select_teams_streaks_stats
from maccabipediabot.games_set_stats_flow.menus_keyboards import create_games_stats_main_menu_keyboard
from maccabipediabot.games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions, GamesStatsMainMenuOptions, \
    PlayersStreaksStatsMenuOptions, \
    MoreStatsOrFinishMenuOptions, TeamStreaksStatsMenuOptions
from maccabipediabot.games_set_stats_flow.players_streaks_stats import show_players_streaks_stats_menu_action, \
    show_players_unbeaten_streaks_action, \
    show_players_winning_streaks_action, show_players_streaks_maccabi_score_at_least_a_goal_action, \
    show_players_players_maccabi_with_clean_sheets_action
from maccabipediabot.games_set_stats_flow.summary_stats import show_summary_stats_action
from maccabipediabot.games_set_stats_flow.teams_streaks_stats import show_teams_streaks_stats_menu_action, \
    show_teams_streak_maccabi_unbeaten_action, \
    show_teams_streaks_maccabi_score_at_least_a_goal_action, show_teams_streaks_maccabi_win_action, \
    show_teams_streaks_maccabi_with_clean_sheets_action
from maccabipediabot.games_set_stats_flow.top_players_stats import show_top_players_stats_menu_action, \
    show_top_scorers_action, \
    show_top_assisters_action, show_most_played_action, show_most_captain_action
from maccabipediabot.handlers_utils import send_typing_action, log_user_request, \
    go_back_to_main_menu_from_conversation_handler
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering
from maccabipediabot.main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, \
    remove_keyboard_reply_markup

logger = logging.getLogger(__name__)


@log_user_request
@send_typing_action
def games_stats_action(update, context):
    # In case the uses got here without filter any games, we should apply the default filter for him
    if _USER_DATE_GAMES_FILTER_KEY not in context.user_data:
        set_default_filters_for_current_user(update, context)

    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    if not games:
        context.bot.send_message(chat_id=update.effective_chat.id, text=GamesStatsMainMenuOptions.NO_GAMES_TEXT,
                                 reply_markup=create_main_user_reply_keyboard())

        return ConversationHandler.END
    else:

        games_filtering = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY])

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{len(games_filtering.filter_games())} משחקים נבחרו, המשחקים שנבחרו:"
                                      f"\n{games_filtering.to_user_description()}",
                                 reply_markup=remove_keyboard_reply_markup())  # This message will re-add the user keyboard

        reply_keyboard = create_games_stats_main_menu_keyboard()
        context.bot.send_message(chat_id=update.effective_chat.id, text=GamesStatsMainMenuOptions.FIRST_TIME_TEXT,
                                 reply_markup=reply_keyboard)
        return show_stats


@log_user_request
@send_typing_action
def finished_to_show_games_stats_action(update, context):
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id,
                             reply_markup=create_main_user_reply_keyboard(),
                             text=f"יצאת ממצב צפייה בסטטיסטיקות"
                                  f"\nלהתראות, <a href='www.maccabipedia.co.il'>מכביפדיה</a>")

    return ConversationHandler.END


def create_games_stats_conversion_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("games_stats", games_stats_action),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GAMES_STATS}$"), games_stats_action)],
        states={
            show_stats: [
                CallbackQueryHandler(show_top_players_stats_menu_action,
                                     pattern=f"^{GamesStatsMainMenuOptions.TOP_PLAYERS_STATS}$"),
                CallbackQueryHandler(show_players_streaks_stats_menu_action,
                                     pattern=f"^{GamesStatsMainMenuOptions.PLAYERS_STREAKS_STATS}$"),
                CallbackQueryHandler(show_teams_streaks_stats_menu_action,
                                     pattern=f"^{GamesStatsMainMenuOptions.TEAMS_STREAKS_STATS}$"),
                CallbackQueryHandler(show_summary_stats_action, pattern=f"^{GamesStatsMainMenuOptions.SUMMARY_STATS}$"),
                CallbackQueryHandler(finished_to_show_games_stats_action,
                                     pattern=f"^{GamesStatsMainMenuOptions.FINISH}$")],

            select_more_stats_or_finish: [
                CallbackQueryHandler(go_back_to_games_stats_main_menu,
                                     pattern=f"^{MoreStatsOrFinishMenuOptions.MORE_STATS}$"),
                CallbackQueryHandler(finished_to_show_games_stats_action,
                                     pattern=f"^{MoreStatsOrFinishMenuOptions.FINISH}$"),
            ],

            select_top_players_stats: [
                CallbackQueryHandler(show_top_scorers_action, pattern=f"^{TopPlayersStatsMenuOptions.TOP_SCORERS}$"),
                CallbackQueryHandler(show_top_assisters_action,
                                     pattern=f"^{TopPlayersStatsMenuOptions.TOP_ASSISTERS}$"),
                CallbackQueryHandler(show_most_captain_action, pattern=f"^{TopPlayersStatsMenuOptions.MOST_CAPTAIN}$"),
                CallbackQueryHandler(show_most_played_action, pattern=f"^{TopPlayersStatsMenuOptions.MOST_PLAYED}$")],

            select_players_streaks_stats: [
                CallbackQueryHandler(show_players_winning_streaks_action,
                                     pattern=f"^{PlayersStreaksStatsMenuOptions.WINNING_STREAK}$"),
                CallbackQueryHandler(show_players_unbeaten_streaks_action,
                                     pattern=f"^{PlayersStreaksStatsMenuOptions.UNBEATEN_STREAK}$"),
                CallbackQueryHandler(show_players_streaks_maccabi_score_at_least_a_goal_action,
                                     pattern=f"^{PlayersStreaksStatsMenuOptions.SCORE_AT_LEAST_A_GOAL}$"),
                CallbackQueryHandler(show_players_players_maccabi_with_clean_sheets_action,
                                     pattern=f"^{PlayersStreaksStatsMenuOptions.CLEAN_SHEETS}$")],

            select_teams_streaks_stats: [
                CallbackQueryHandler(show_teams_streaks_maccabi_win_action,
                                     pattern=f"^{TeamStreaksStatsMenuOptions.WINNING_STREAK}$"),
                CallbackQueryHandler(show_teams_streak_maccabi_unbeaten_action,
                                     pattern=f"^{TeamStreaksStatsMenuOptions.UNBEATEN_STREAK}$"),
                CallbackQueryHandler(show_teams_streaks_maccabi_score_at_least_a_goal_action,
                                     pattern=f"^{TeamStreaksStatsMenuOptions.SCORE_AT_LEAST_A_GOAL}$"),
                CallbackQueryHandler(show_teams_streaks_maccabi_with_clean_sheets_action,
                                     pattern=f"^{TeamStreaksStatsMenuOptions.CLEAN_SHEETS}$")],

        },
        fallbacks=[MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"),
                                  go_back_to_main_menu_from_conversation_handler)]
    )
