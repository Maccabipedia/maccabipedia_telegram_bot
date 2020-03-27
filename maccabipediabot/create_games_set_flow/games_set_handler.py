import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from maccabipediabot.common import _USER_DATE_GAMES_FILTER_KEY, set_default_filters_for_current_user
from maccabipediabot.create_games_set_flow.coach_filtering_menu import show_coach_menu_action, save_coach_decision, save_specific_coach_action
from maccabipediabot.create_games_set_flow.common_menu import go_back_to_main_games_filter_menu
from maccabipediabot.create_games_set_flow.competition_filtering_menu import show_competition_menu_action, save_competition_decision
from maccabipediabot.create_games_set_flow.date_filtering_menu import show_date_menu_action, save_date_decision
from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import *
from maccabipediabot.create_games_set_flow.home_away_filtering_menu import show_home_away_menu_action, save_home_away_decision
from maccabipediabot.create_games_set_flow.menus_keyboards import create_games_filter_main_menu, create_finish_or_continue_games_filter_menu
from maccabipediabot.create_games_set_flow.menus_options import GamesFilteringMainMenuOptions, FinishOrContinueFilteringMenuOptions
from maccabipediabot.create_games_set_flow.played_player_filtering_menu import show_played_player_menu_action, save_played_player_decision, \
    save_specific_played_player_action
from maccabipediabot.create_games_set_flow.referee_filtering_menu import show_referee_menu_action, save_referee_decision, save_specific_referee_action
from maccabipediabot.create_games_set_flow.stadium_filtering_menu import show_stadium_menu_action, save_stadium_decision, save_specific_stadium_action
from maccabipediabot.create_games_set_flow.team_filtering_menu import show_team_menu_action, save_team_decision, save_specific_team_action
from maccabipediabot.handlers_utils import send_typing_action, log_user_request
from maccabipediabot.maccabi_games import get_maccabipedia_games
from maccabipediabot.maccabi_games_filtering import MaccabiGamesFiltering
from maccabipediabot.main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard

logger = logging.getLogger(__name__)


@log_user_request
@send_typing_action
def create_games_set(update, context):
    """
    Creates a games set that will be used for statistics
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"מתחילים ליצור קבוצת משחקים, {len(get_maccabipedia_games())} משחקים קיימים")
    set_default_filters_for_current_user(update, context)  # In case he want to exit with all games (unfiltered)

    reply_keyboard = create_games_filter_main_menu(first_time_menu=True)

    # This is the entry point of games filtering, we will show the user a general msg asking him to filter games
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesFilteringMainMenuOptions.FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return games_filtering


@log_user_request
@send_typing_action
def unknown_message_show_finish_or_continue_menu_action(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"הפקודה האחרונה לא הובנה")

    reply_keyboard = create_finish_or_continue_games_filter_menu()
    context.bot.send_message(chat_id=update.effective_chat.id, text=FinishOrContinueFilteringMenuOptions.TEXT, reply_markup=reply_keyboard)

    return finish_or_continue


@log_user_request
@send_typing_action
def continue_to_filter_games(update, context):
    return go_back_to_main_games_filter_menu(update, context)


@log_user_request
@send_typing_action
def finished_to_create_games_action(update, context):
    filtered_games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()

    query = update.callback_query
    query.edit_message_text(text=f"סיימת לסנן משחקים, {len(filtered_games)} משחקים נבחרו!")

    context.bot.send_message(chat_id=update.effective_chat.id, text=" בכדי להמשיך לחץ מטה על 'סטטיסטיקה'",
                             reply_markup=create_main_user_reply_keyboard())

    return ConversationHandler.END


def create_games_set_conversion_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("create_games_set", create_games_set),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GAMES_FILTERING}$"), create_games_set)],
        states={
            games_filtering: [CallbackQueryHandler(show_home_away_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.HOME_AWAY}$"),
                              CallbackQueryHandler(show_team_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.TEAM}$"),
                              CallbackQueryHandler(show_competition_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.COMPETITION}$"),
                              CallbackQueryHandler(show_date_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.DATE}$"),
                              CallbackQueryHandler(show_played_player_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.PLAYED_PLAYER}$"),
                              CallbackQueryHandler(show_referee_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.REFEREE}$"),
                              CallbackQueryHandler(show_stadium_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.STADIUM}$"),
                              CallbackQueryHandler(show_coach_menu_action, pattern=f"^{GamesFilteringMainMenuOptions.COACH}$"),
                              CallbackQueryHandler(finished_to_create_games_action, pattern=f"^{GamesFilteringMainMenuOptions.FINISH}$")],

            select_home_away_filter: [CallbackQueryHandler(save_home_away_decision)],
            select_team_filter: [CallbackQueryHandler(save_team_decision),
                                 MessageHandler(Filters.all, save_specific_team_action)],
            select_competition_filter: [CallbackQueryHandler(save_competition_decision)],
            select_date_filter: [CallbackQueryHandler(save_date_decision)],
            select_played_player_filter: [CallbackQueryHandler(save_played_player_decision),
                                          MessageHandler(Filters.all, save_specific_played_player_action)],
            select_referee_filter: [CallbackQueryHandler(save_referee_decision),
                                    MessageHandler(Filters.all, save_specific_referee_action)],
            select_stadium_filter: [CallbackQueryHandler(save_stadium_decision),
                                    MessageHandler(Filters.all, save_specific_stadium_action)],
            select_coach_filter: [CallbackQueryHandler(save_coach_decision),
                                  MessageHandler(Filters.all, save_specific_coach_action)],

            finish_or_continue: [CallbackQueryHandler(finished_to_create_games_action, pattern=f"^{FinishOrContinueFilteringMenuOptions.FINISH}$"),
                                 CallbackQueryHandler(continue_to_filter_games, pattern=f"^{FinishOrContinueFilteringMenuOptions.CONTINUE}$")]

        },
        fallbacks=[MessageHandler(Filters.all, unknown_message_show_finish_or_continue_menu_action)]
    )
