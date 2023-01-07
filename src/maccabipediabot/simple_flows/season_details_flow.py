from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from maccabipediabot.common import format_season_id, extract_season_details_from_maccabipedia_as_html_text
from maccabipediabot.handlers_utils import log_user_request, send_typing_action, \
    go_back_to_main_menu_from_conversation_handler
from maccabipediabot.main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, \
    create_go_back_reply_keyboard

_show_season_details_state = range(1)


@log_user_request
@send_typing_action
def show_season_details_handler(update, context):
    """
    Shows the given season details, such as wins/losses/ties amount and which titles maccabi won in this season
    """
    full_season_id = format_season_id(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                             text=extract_season_details_from_maccabipedia_as_html_text(full_season_id),
                             reply_markup=create_main_user_reply_keyboard())

    return ConversationHandler.END


@log_user_request
@send_typing_action
def season_details_entry_point(update, context):
    """
    The entry point of show season details process, we ask the season id from the user
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_go_back_reply_keyboard(),
                             text=f"הקלד את העונה עבורה תרצה לקבל מידע,"
                                  f"\nלמשל 1995/96, 1996 או 96:")

    return _show_season_details_state


def create_season_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("season", season_details_entry_point),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.SEASON_STATS}$"),
                                     season_details_entry_point)],
        states={_show_season_details_state: [
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"),
                           go_back_to_main_menu_from_conversation_handler),
            MessageHandler(Filters.text, show_season_details_handler)]},
        fallbacks=[MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"),
                                  go_back_to_main_menu_from_conversation_handler)]
    )
