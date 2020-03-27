from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from maccabipediabot.common import get_song_lyrics
from maccabipediabot.handlers_utils import log_user_request, send_typing_action, go_back_to_main_menu_from_conversation_handler
from maccabipediabot.main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, create_go_back_reply_keyboard

_show_song_details_state = range(1)


@log_user_request
@send_typing_action
def show_song_details_handler(update, context):
    """
    :return: Lyrics of the given song & link to the page
    """
    song_name = update.message.text
    # TODO: We might want to stay in the same state if we could not find the song (so the user wont need to press on the keyboard again)
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=get_song_lyrics(song_name),
                             reply_markup=create_main_user_reply_keyboard())

    return ConversationHandler.END


@log_user_request
@send_typing_action
def song_details_entry_point(update, context):
    """
    The entry point of show song details process, we ask the song name from the user in this step.
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_go_back_reply_keyboard(),
                             text=f"הקלד את שם השיר עבורו תרצה לקבל מידע:")

    return _show_song_details_state


def create_song_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("song", song_details_entry_point),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.SONG}$"), song_details_entry_point)],
        states={_show_song_details_state: [
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler),
            MessageHandler(Filters.text, show_song_details_handler)]},
        fallbacks=[MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler)]
    )
