from telegram import ParseMode
from telegram.ext import ConversationHandler

from maccabipediabot.games_set_stats_flow.menus_keyboards import create_games_stats_main_menu_keyboard, create_more_stats_or_finish_menu_keyboard
from maccabipediabot.games_set_stats_flow.menus_options import GamesStatsMainMenuOptions, MoreStatsOrFinishMenuOptions
from maccabipediabot.handlers_utils import log_user_request, send_typing_action
from maccabipediabot.games_set_stats_flow.games_stats_conversation_handler_states import show_stats, select_more_stats_or_finish


def go_back_to_games_stats_main_menu(update, context):
    reply_keyboard = create_games_stats_main_menu_keyboard()

    # This is not the first time the user sees this menu, adapt the tet accordingly
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesStatsMainMenuOptions.AFTER_FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return show_stats


def go_to_more_stats_or_finish_menu(update, context):
    reply_keyboard = create_more_stats_or_finish_menu_keyboard()

    context.bot.send_message(chat_id=update.effective_chat.id, text=MoreStatsOrFinishMenuOptions.TEXT, reply_markup=reply_keyboard)
    return select_more_stats_or_finish


@log_user_request
@send_typing_action
def finished_to_show_games_stats_action(update, context):
    context.bot.send_message(parse_mode=ParseMode.HTML, chat_id=update.effective_chat.id,
                             text=f"יצאת ממצב צפייה בסטטיסטיקות"
                                  f"\n להתראות, <a href='www.maccabipedia.co.il'>מכביפדיה</a>")

    return ConversationHandler.END
