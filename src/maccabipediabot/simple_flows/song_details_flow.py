from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from common import get_song_lyrics
from handlers_utils import log_user_request, send_typing_action, go_back_to_main_menu_from_conversation_handler
from main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, create_go_back_reply_keyboard
from similar_song_matcher import song_exists_on_maccabipedia, SimilarMaccabiPediaSong

_show_song_details_state = range(1)


@log_user_request
@send_typing_action
def show_song_details_handler(update, context):
    """
    :return: Lyrics of the given song & link to the page
    """
    song_name = update.message.text

    if not song_exists_on_maccabipedia(song_name):
        similar_songs_pages_names = SimilarMaccabiPediaSong(song_name).find_most_similar_songs()
        if similar_songs_pages_names:
            pretty_print_of_similar_songs_pages = "\n".join(page_name for page_name in similar_songs_pages_names)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"לא נמצא שיר בשם: '{song_name}', אלו השירים עם השם הדומה ביותר:"
                                                                            f"\n{pretty_print_of_similar_songs_pages}"
                                                                            f"\n\nשלח את שם השיר הרצוי")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"לא נמצא שיר בשם: '{song_name}' נסה בשנית")

        return _show_song_details_state
    else:  # This song exists on maccabipedia, lets show it!
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
