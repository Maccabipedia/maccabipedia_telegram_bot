from telegram import ParseMode

from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY, transform_players_with_maccabi_games_to_telegram_html_text
from maccabipediabot.games_set_stats_flow.common_menu import go_to_more_stats_or_finish_menu
from maccabipediabot.games_set_stats_flow.games_stats_conversation_handler_states import select_players_streaks_stats
from maccabipediabot.games_set_stats_flow.menus_keyboards import create_players_streaks_games_stats_keyboard
from maccabipediabot.games_set_stats_flow.menus_options import PlayersStreaksStatsMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_players_streaks_stats_menu_action(update, context):
    reply_keyboard = create_players_streaks_games_stats_keyboard()

    query = update.callback_query
    query.edit_message_text(text=PlayersStreaksStatsMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_players_streaks_stats


@log_user_request
@send_typing_action
def show_players_unbeaten_streaks_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players_streaks.get_players_with_best_unbeaten_streak()
    top_players_html_text = transform_players_with_maccabi_games_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים עם רצף 'לא מנוצחים' הארוך ביותר: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_players_winning_streaks_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players_streaks.get_players_with_best_win_streak()
    top_players_html_text = transform_players_with_maccabi_games_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים עם רצף הנצחונות הארוך ביותר: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_players_streaks_maccabi_score_at_least_a_goal_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players_streaks.get_players_with_best_maccabi_score_goal_streak()
    top_players_html_text = transform_players_with_maccabi_games_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים עם רצף 'מכבי הבקיעה לפחות גול אחד' הארוך ביותר: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_players_players_maccabi_with_clean_sheets_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players_streaks.get_players_with_best_clean_sheets_streak()
    top_players_html_text = transform_players_with_maccabi_games_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים עם רצף 'מכבי שמרה על רשת נקייה' הארוך ביותר: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)
