from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import select_played_player_filter
from maccabipediabot.create_games_set_flow.common_menu import get_button_text_from_query_data, go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_keyboards import create_played_player_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import PlayedPlayerFilteringMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games import maccabipedia_games, get_similar_player_names
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_played_player_menu_action(update, context):
    reply_keyboard = create_played_player_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=PlayedPlayerFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_played_player_filter


@log_user_request
@send_typing_action
def save_played_player_decision(update, context):
    query = update.callback_query

    if query.data == PlayedPlayerFilteringMenuOptions.ALL_PLAYERS:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_player_filter_to_all_players()
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")

        return go_back_to_main_games_filter_menu(update, context)
    else:
        query.edit_message_text(text="הקלד את שם השחקן:")
        return select_played_player_filter


@log_user_request
@send_typing_action
def save_specific_played_player_action(update, context):
    user_player_name = update.message.text

    if user_player_name not in maccabipedia_games.available_players_names:
        similar_players_names = get_similar_player_names(user_player_name)
        if similar_players_names:
            pretty_print_of_similar_players_names = "\n".join(player_name for player_name in similar_players_names)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"שחקן בשם {user_player_name} לא נמצא, אלו בעלי השם הדומה ביותר:\n"
                                          f"{pretty_print_of_similar_players_names}"
                                          f"\n\nשלח את שם השחקן הרצוי:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"שחקן בשם {user_player_name} לא נמצא, נסה בשנית")

        return select_played_player_filter
    else:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_played_player_filter(user_player_name)
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"בחרת ב: {user_player_name}, {len(games)} משחקים נבחרו")
        return go_back_to_main_games_filter_menu(update, context)
