from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.common_menu import get_button_text_from_query_data, \
    go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import select_stadium_filter
from maccabipediabot.create_games_set_flow.menus_keyboards import create_stadium_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import StadiumFilteringMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games import get_maccabipedia_games, get_similar_stadiums_names
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_stadium_menu_action(update, context):
    reply_keyboard = create_stadium_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=StadiumFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_stadium_filter


@log_user_request
@send_typing_action
def save_stadium_decision(update, context):
    query = update.callback_query

    if query.data == StadiumFilteringMenuOptions.ALL_STADIUMS:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_stadium_filter_to_all_stadiums()
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")

        return go_back_to_main_games_filter_menu(update, context)
    else:
        query.edit_message_text(text="הקלד את שם האצטדיון:")
        return select_stadium_filter


@log_user_request
@send_typing_action
def save_specific_stadium_action(update, context):
    user_stadium = update.message.text

    if user_stadium not in get_maccabipedia_games().available_stadiums:
        similar_stadiums_names = get_similar_stadiums_names(user_stadium)
        if similar_stadiums_names:
            pretty_print_of_similar_stadiums_names = "\n".join(stadium_name for stadium_name in similar_stadiums_names)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"אצטדיון בשם {user_stadium} לא נמצא, אלו בעלי השם הדומה ביותר:\n"
                                          f"{pretty_print_of_similar_stadiums_names}"
                                          f"\n\nשלח את שם האצטדיון הרצוי:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"אצטדיון בשם {user_stadium} לא נמצא, נסה בשנית")

        return select_stadium_filter
    else:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_stadium_filter(user_stadium)
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"בחרת ב: {user_stadium}, {len(games)} משחקים נבחרו")
        return go_back_to_main_games_filter_menu(update, context)
