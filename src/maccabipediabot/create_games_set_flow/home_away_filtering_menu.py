from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.common_menu import get_button_text_from_query_data, \
    go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import select_home_away_filter
from maccabipediabot.create_games_set_flow.menus_keyboards import create_home_away_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import HomeAwayFilteringMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_home_away_menu_action(update, context):
    reply_keyboard = create_home_away_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=HomeAwayFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_home_away_filter


@log_user_request
@send_typing_action
def save_home_away_decision(update, context):
    query = update.callback_query
    context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_home_away_filter(query.data)
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

    button_text_the_user_chose = get_button_text_from_query_data(query)
    query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")
    # Showing the main menu and moving to the step of choosing a game filter again
    return go_back_to_main_games_filter_menu(update, context)
