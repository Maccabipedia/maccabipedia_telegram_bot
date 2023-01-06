from telegram import ParseMode

from common import _USER_DATE_GAMES_FILTER_KEY, transform_players_with_amount_to_telegram_html_text
from games_set_stats_flow.common_menu import go_to_more_stats_or_finish_menu
from games_set_stats_flow.games_stats_conversation_handler_states import select_top_players_stats
from games_set_stats_flow.menus_keyboards import create_top_players_games_stats_keyboard
from games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions
from handlers_utils import log_user_request, send_typing_action
from maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_top_players_stats_menu_action(update, context):
    reply_keyboard = create_top_players_games_stats_keyboard()

    query = update.callback_query
    query.edit_message_text(text=TopPlayersStatsMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_top_players_stats


@log_user_request
@send_typing_action
def show_top_scorers_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players.best_scorers[0:10]
    top_players_html_text = transform_players_with_amount_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"הכובשים המובילים: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_top_assisters_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players.best_assisters[0:10]
    top_players_html_text = transform_players_with_amount_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"המבשלים המובילים: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_most_played_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players.most_played[0:10]
    top_players_html_text = transform_players_with_amount_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים עם הכי הרבה הופעות: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)


@log_user_request
@send_typing_action
def show_most_captain_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    top = games.players.most_captains[0:10]
    top_players_html_text = transform_players_with_amount_to_telegram_html_text(top)

    query = update.callback_query
    query.edit_message_text(parse_mode=ParseMode.HTML, text=f"השחקנים שהיו קפטן הכי הרבה פעמים: \n{top_players_html_text}")

    return go_to_more_stats_or_finish_menu(update, context)
