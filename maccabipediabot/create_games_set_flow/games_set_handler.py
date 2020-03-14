import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from maccabipediabot.consts import _USER_DATE_GAMES_FILTER_KEY
from maccabipediabot.create_games_set_flow.menus_keyboards import create_games_filter_main_menu, create_home_away_games_filter_menu, \
    create_team_games_filter_menu, create_competition_games_filter_menu, create_date_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import GamesFilteringMainMenuOptions, TeamFilteringMenuOptions, \
    CompetitionFilteringMenuOptions, DateFilteringMenuOptions, HomeAwayFilteringMenuOptions
from maccabipediabot.general_handlers import help_handler
from maccabipediabot.handlers_utils import send_typing_action, log_user_request
from maccabipediabot.maccabi_games import maccabipedia_games, get_similar_teams_names
from maccabipediabot.maccabi_games_filtering import GamesFilter, MaccabiGamesFiltering

logger = logging.getLogger(__name__)

select_games_filter, games_filtering, select_home_away_filter, select_team_filter, select_competition_filter, select_date_filter = range(6)


def get_button_text_from_query_data(query):
    from itertools import chain

    return next(button.text for button in chain.from_iterable(query.message.reply_markup.inline_keyboard) if button.callback_data == query.data)


def go_back_to_main_games_filter_menu(update, context):
    reply_keyboard = create_games_filter_main_menu(first_time_menu=False)

    # This is not the first time the user sees the games filtering menu, we will ask him if he want to continue filtering or to finish the process.
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesFilteringMainMenuOptions.AFTER_FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return games_filtering


def set_default_filters_for_current_user(update, context):
    context.user_data[_USER_DATE_GAMES_FILTER_KEY] = GamesFilter()


@log_user_request
@send_typing_action
def create_games_set(update, context):
    """
    Creates a games set that will be used for statistics
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="מתחילים ליצור קבוצת משחקים")
    set_default_filters_for_current_user(update, context)  # In case he want to exit with all games (unfiltered)

    reply_keyboard = create_games_filter_main_menu(first_time_menu=True)

    # This is the entry point of games filtering, we will show the user a general msg asking him to filter games
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesFilteringMainMenuOptions.FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return games_filtering


@log_user_request
@send_typing_action
def show_date_menu_action(update, context):
    reply_keyboard = create_date_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=DateFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_date_filter


@log_user_request
@send_typing_action
def save_date_decision(update, context):
    query = update.callback_query
    context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_date_filter(query.data)

    button_text_the_user_chose = get_button_text_from_query_data(query)
    query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}")
    # Showing the main menu and moving to the step of choosing a game filter again
    return go_back_to_main_games_filter_menu(update, context)


@log_user_request
@send_typing_action
def show_competition_menu_action(update, context):
    reply_keyboard = create_competition_games_filter_menu()

    query = update.callback_query
    query.edit_message_text(text=CompetitionFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return select_competition_filter


@log_user_request
@send_typing_action
def save_competition_decision(update, context):
    query = update.callback_query
    context.user_data[_USER_DATE_GAMES_FILTER_KEY].update_competition_filter(query.data)

    button_text_the_user_chose = get_button_text_from_query_data(query)
    query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}")
    # Showing the main menu and moving to the step of choosing a game filter again
    return go_back_to_main_games_filter_menu(update, context)


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

    button_text_the_user_chose = get_button_text_from_query_data(query)
    query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}")
    # Showing the main menu and moving to the step of choosing a game filter again
    return go_back_to_main_games_filter_menu(update, context)


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

        button_text_the_user_chose = get_button_text_from_query_data(query)
        query.edit_message_text(text=f"בחרת ב: {button_text_the_user_chose}")

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

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"בחרת ב: {team_name}")
        return go_back_to_main_games_filter_menu(update, context)


@log_user_request
@send_typing_action
def finished_to_create_games_action(update, context):
    filtered_games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{len(filtered_games)} משחקים נבחרו,"
                                                                    f"\nבכדי לראות סטטיסטיקות על המשחקים שנבחרו בחר:"
                                                                    f"\n/games_stats")

    return ConversationHandler.END


def create_games_set_conversion_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("create_games_set", create_games_set)],
        states={
            games_filtering: [CallbackQueryHandler(show_home_away_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.HOME_AWAY}$"),
                              CallbackQueryHandler(show_team_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.TEAM}$"),
                              CallbackQueryHandler(show_competition_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.COMPETITION}$"),
                              CallbackQueryHandler(show_date_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.DATE}$"),
                              CallbackQueryHandler(finished_to_create_games_action, pattern=f"^{GamesFilteringMainMenuOptions.FINISH}$")],

            select_home_away_filter: [CallbackQueryHandler(save_home_away_decision)],
            select_team_filter: [CallbackQueryHandler(save_team_decision), MessageHandler(Filters.all, save_specific_team_action)],
            select_competition_filter: [CallbackQueryHandler(save_competition_decision)],
            select_date_filter: [CallbackQueryHandler(save_date_decision)],

        },
        fallbacks=[CommandHandler('help', help_handler)]
    )
