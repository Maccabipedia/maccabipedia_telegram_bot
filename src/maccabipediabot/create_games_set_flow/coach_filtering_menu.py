from telegram.parsemode import ParseMode

from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.common_menu import get_button_text_from_query_data, \
    go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import select_coach_filter
from maccabipediabot.create_games_set_flow.menus_keyboards import create_coach_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import CoachFilteringMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games import get_maccabipedia_games, get_similar_coaches_names
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_coach_menu_action(update, context):
    reply_keyboard = create_coach_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=CoachFilteringMenuOptions.HTML_TEXT, parse_mode=ParseMode.HTML,
                            reply_markup=reply_keyboard)

    return select_coach_filter


@log_user_request
@send_typing_action
def save_coach_decision(update, context):
    query = update.callback_query

    if query.data == CoachFilteringMenuOptions.ALL_COACHES:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_coach_filter_to_all_coaches()
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")

        return go_back_to_main_games_filter_menu(update, context)
    else:
        query.edit_message_text(text="הקלד את שם המאמן הרצוי:")
        return select_coach_filter


@log_user_request
@send_typing_action
def save_specific_coach_action(update, context):
    user_coach = update.message.text

    if user_coach not in get_maccabipedia_games().available_coaches:
        similar_coaches_names = get_similar_coaches_names(user_coach)
        if similar_coaches_names:
            pretty_print_of_similar_coaches_names = "\n".join(coach_name for coach_name in similar_coaches_names)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'לא נמצא מאמן בשם "{user_coach}", מאמנים בעלי שם דומה:'
                                          f"\n{pretty_print_of_similar_coaches_names}"
                                          f"\n\nהקלד את שם המאמן הרצוי:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'לא נמצא מאמן בשם "{user_coach}", נסה בשנית:')

        return select_coach_filter
    else:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_coach_filter(user_coach)
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"בחרת ב: {user_coach}, {len(games)} משחקים נבחרו")
        return go_back_to_main_games_filter_menu(update, context)
