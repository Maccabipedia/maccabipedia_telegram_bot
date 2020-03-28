from telegram import ParseMode, InputMediaPhoto
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from maccabipediabot.common import format_season_id, extract_season_uniforms_from_maccabipedia
from maccabipediabot.handlers_utils import log_user_request, send_typing_action, go_back_to_main_menu_from_conversation_handler, \
    send_upload_image_action
from maccabipediabot.main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, create_go_back_reply_keyboard

_show_uniforms_state = range(1)


@log_user_request
@send_upload_image_action
def show_uniforms_handler(update, context):
    """
    Shows the given uniforms (by the chosen season).
    """
    full_season_id = format_season_id(update.message.text)
    html_text, uniforms = extract_season_uniforms_from_maccabipedia(full_season_id)
    input_media_uniforms = [InputMediaPhoto(photo_url) for photo_url in uniforms]
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=html_text,
                             reply_markup=create_main_user_reply_keyboard())
    if input_media_uniforms:
        context.bot.send_media_group(chat_id=update.effective_chat.id, media=input_media_uniforms)

    return ConversationHandler.END


@log_user_request
@send_typing_action
def uniforms_entry_point(update, context):
    """
    The entry point of showing any uniforms to the user
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_go_back_reply_keyboard(),
                             text=f"הקלד את העונה עבורה תרצה לקבל את המדים"
                                  f"\nלמשל 1995/96, 1996 או 96:")

    return _show_uniforms_state


def create_uniforms_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("uniforms", uniforms_entry_point),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.UNIFORMS}$"), uniforms_entry_point)],
        states={_show_uniforms_state: [
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler),
            MessageHandler(Filters.text, show_uniforms_handler)]},
        fallbacks=[MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler)]
    )
