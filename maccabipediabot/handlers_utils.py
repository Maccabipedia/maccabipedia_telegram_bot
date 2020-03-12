import logging
from functools import wraps

from telegram import ChatAction

logger = logging.getLogger(__name__)


def send_typing_action(func):
    """
    Send "Typing..." to the user while processing the request
    """

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func
