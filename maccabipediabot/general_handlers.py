import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.parsemode import ParseMode

from maccabipediabot.common import create_maccabipedia_shirt_number_category_html_text, get_song_lyrics
from maccabipediabot.handlers_utils import send_typing_action, log_user_request


logger = logging.getLogger(__name__)


def error_callback(update, context):
    """
    Handle all telegram bot related errors
    """
    logger.exception("Encountered an error")
    try:
        raise context.error
    except Unauthorized:
        pass
        # remove update.message.chat_id from conversation list
    except BadRequest:
        pass
        # handle malformed requests - read more below!
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated as e:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors


@log_user_request
@send_typing_action
def help_handler(update, context):
    """
    Shows the help for this bot.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="בכדי לבחור את קבוצת המשחקים שעליהם תרצה לקבל סטטיסטיקה:"
                                                                    "\n/create_games_set"
                                                                    "\n\nבכדי לצפות בסטטיסטיקות כלשהן:"
                                                                    "\n/games_set"
                                                                    "\n\nקבלת השחקנים ששיחקו עם מספר חולצה כלשהו, נניח 10:"
                                                                    f"\n/shirt_number 10")


@log_user_request
@send_typing_action
def unknown_message_handler(update, context):
    """
    For any msg that we didn't registered explicit
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="הפקודה האחרונה לא הובנה, נסו להשתמש ב: /help")


@log_user_request
@send_typing_action
def start_handler(update, context):
    """
    First msg the user sees
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"שלום {update.effective_chat.username}")

    help_handler(update, context)


@log_user_request
@send_typing_action
def shirt_number_handler(update, context):
    """
    Send link ot the category of player who played with the given shirt number
    """
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"מספר חולצה לא התקבל, בכדי לבדוק למשל אילו שחקנים שיחקו עם חולצה מספר 10, שלח:"
                                      f"\n/shirt_number 10")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=create_maccabipedia_shirt_number_category_html_text(context.args[0]))

@log_user_request
@send_typing_action
def song_handler(update, context):
    """
    :return: Lyrics of the given song & link to the page
    """

    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"שם שיר לא התקבל. בכדי לקבל מילות שיר, למשל, שיר הקונטרה, שלח:"
                                      f"\n/song הקונטרה")
    else:
        song_name = "_".join(context.args[:])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=get_song_lyrics(song_name))