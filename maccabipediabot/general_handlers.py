import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.parsemode import ParseMode

from maccabipediabot.common import create_maccabipedia_shirt_number_category_html_text
from maccabipediabot.handlers_utils import send_typing_action, log_user_request
from maccabipediabot.main_user_keyboard import create_main_user_reply_keyboard

logger = logging.getLogger(__name__)


def error_callback(update, context):
    """
    Handle all telegram bot related errors
    """
    logger.error("Encountered an error, handling it inside error_callback")
    try:
        raise context.error
    except Unauthorized as e:
        # remove update.message.chat_id from conversation list
        logger.error(e)
    except BadRequest as e:
        # handle malformed requests - read more below!
        logger.error(e)
    except TimedOut as e:
        # handle slow connection problems
        logger.error(e)
    except NetworkError as e:
        # handle other connection problems
        logger.error(e)
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.error(e)
    except TelegramError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


@log_user_request
@send_typing_action
def help_handler(update, context):
    """
    Shows the help for this bot.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                             text=f"בכדי לקבל סטטיסטיקות, השתמש בתפריט מטה ולחץ על:"
                                  f"\n1) 'סנן משחקים' בכדי להחליט אילו משחקים לכלול"
                                  f"\n2) לחץ על 'סטטיסטיקה'"
                                  f"\n\nתוכל לעיין באופציות נוספות בתפריט שנפתח מטה."
                                  f"\nבכל שלב ניתן לחזור לתפריט העזר באמצעות הפקודה: /help"
                                  f"\nבתודה, <a href='www.maccabipedia.co.il'>מכביפדיה.</a>")


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
    user_name = update.effective_chat.username
    if user_name is not None:
        hello_message = f"שלום {user_name}."
    else:
        hello_message = f"שלום."

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{hello_message}", reply_markup=create_main_user_reply_keyboard())

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
