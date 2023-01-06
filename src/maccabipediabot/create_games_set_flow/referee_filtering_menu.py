from common import _USER_DATE_GAMES_FILTER_KEY
from create_games_set_flow.common_menu import get_button_text_from_query_data, go_back_to_main_games_filter_menu
from create_games_set_flow.games_set_conversation_handler_states import select_referee_filter
from create_games_set_flow.menus_keyboards import create_referee_games_filter_menu
from create_games_set_flow.menus_options import RefereeFilteringMenuOptions
from handlers_utils import log_user_request, send_typing_action
from maccabi_games import get_maccabipedia_games, get_similar_referees_names
from maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_referee_menu_action(update, context):
    reply_keyboard = create_referee_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=RefereeFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_referee_filter


@log_user_request
@send_typing_action
def save_referee_decision(update, context):
    query = update.callback_query

    if query.data == RefereeFilteringMenuOptions.ALL_REFEREES:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_referee_filter_to_all_referees()
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")

        return go_back_to_main_games_filter_menu(update, context)
    else:
        query.edit_message_text(text="הקלד את שם השופט הרצוי:")
        return select_referee_filter


@log_user_request
@send_typing_action
def save_specific_referee_action(update, context):
    user_referee = update.message.text

    if user_referee not in get_maccabipedia_games().available_referees:
        similar_referees_names = get_similar_referees_names(user_referee)
        if similar_referees_names:
            pretty_print_of_similar_referees_names = "\n".join(referee_name for referee_name in similar_referees_names)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'לא נמצא שופט בשם "{user_referee}", מאמנים בעלי שם דומה:'
                                          f"{pretty_print_of_similar_referees_names}"
                                          f"\n\nהקלד את שם השופט הרצוי:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"שופט בשם {user_referee} לא נמצא, נסה בשנית")

        return select_referee_filter
    else:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_referee_filter(user_referee)
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"בחרת ב: {user_referee}, {len(games)} משחקים נבחרו")
        return go_back_to_main_games_filter_menu(update, context)
