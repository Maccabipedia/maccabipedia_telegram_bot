import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from maccabipediabot.handlers_utils import send_typing_action

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


@send_typing_action
def help_handler(update, context):
    """
    Shows the help for this bot.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="בכדי לבחור את המשחקים שעליהם תרצה לקבל סטטיסטיקה:"
                                                                    "\n/create_games_set")


@send_typing_action
def unknown_message_handler(update, context):
    """
    For any msg that we didn't registered explicit
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="הפקודה אחרונה לא הובנה, נסו להשתמש ב: /help")


@send_typing_action
def start_handler(update, context):
    """
    First msg the user sees
    """
    logger.info(f"New user interacts with the bot: {update.effective_chat.username}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"שלום {update.effective_chat.username}")

    help_handler(update, context)
