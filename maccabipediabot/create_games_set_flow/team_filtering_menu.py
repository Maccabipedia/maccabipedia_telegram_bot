from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import select_team_filter
from maccabipediabot.create_games_set_flow.common_menu import get_button_text_from_query_data, go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_keyboards import create_team_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import TeamFilteringMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.maccabi_games import maccabipedia_games, get_similar_teams_names
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_team_menu_action(update, context):
    reply_keyboard = create_team_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=TeamFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)
    return select_team_filter


@log_user_request
@send_typing_action
def save_team_decision(update, context):
    query = update.callback_query

    if query.data == TeamFilteringMenuOptions.ALL_TEAMS:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_team_filter_for_all_teams()
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}, {len(games)} משחקים נבחרו")

        return go_back_to_main_games_filter_menu(update, context)
    else:
        query.edit_message_text(text="הקלד את שם הקבוצה:")
        return select_team_filter


@log_user_request
@send_typing_action
def save_specific_team_action(update, context):
    team_name = update.message.text

    if team_name not in maccabipedia_games.available_opponents:
        similar_team_names = get_similar_teams_names(team_name)
        if similar_team_names:
            pretty_print_of_similar_team_names = "\n".join(team for team in similar_team_names)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"קבוצה בשם {team_name} לא נמצאה, אלו בעלות השם הדומה ביותר:\n"
                                          f"{pretty_print_of_similar_team_names}"
                                          f"\n\nשלח את שם הקבוצה הרצויה:")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"קבוצה בשם {team_name} לא נמצאה, נסה בשנית")

        return select_team_filter
    else:
        context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_team_filter(team_name)
        games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"בחרת ב: {team_name}, {len(games)} משחקים נבחרו")
        return go_back_to_main_games_filter_menu(update, context)
