import os

from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from handlers_utils import log_user_request, send_typing_action, go_back_to_main_menu_from_conversation_handler
from main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, create_go_back_reply_keyboard

_process_feedback_state = range(1)


@log_user_request
@send_typing_action
def process_feedback_handler(update, context):
    """
    Process the user feedback (forward the feedback to some chat)
    """
    feedback_group = os.environ['FEEDBACK_TELEGRAM_GROUP_ID']

    context.bot.forward_message(chat_id=feedback_group, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="תודה רבה!", reply_markup=create_main_user_reply_keyboard())

    return ConversationHandler.END


@log_user_request
@send_typing_action
def feedback_entry_point(update, context):
    """
    Entry point of the process that allows the user to write us feedback
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_go_back_reply_keyboard(),
                             parse_mode=ParseMode.HTML,
                             text=f"נשמח לשמוע כל הערה, הצעה ורעיון לשיפור,"
                                  f"\nעל הבוט או על <a href='www.maccabipedia.co.il'>מכביפדיה</a>:")

    return _process_feedback_state


def create_feedback_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_entry_point),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.FEEDBACK}$"), feedback_entry_point)],
        states={_process_feedback_state: [
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler),
            MessageHandler(Filters.text, process_feedback_handler)]},
        fallbacks=[
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler)]
    )
