import logging

from decorator import decorator
from telegram import ChatAction

logger = logging.getLogger(__name__)


@decorator
def log_user_request(func, update, context, *args, **kwargs):
    """
    Logs the current activity of the user.
    :param func: Function to decorate
    :type func: callable
    :type update: telegram.update.Update
    :type context: telegram.ext.callbackcontext.CallbackContext
    """
    if update.callback_query:
        user_text = update.callback_query.data
    elif context.args:
        user_text = " ".join(context.args)
    else:
        user_text = ""

    logger.info(f"User: {update.effective_chat.username} (id: {update.effective_chat.id}), Function: {func.__name__}, Text: {user_text} ")
    try:
        return func(update, context, *args, **kwargs)
    except Exception:
        logger.exception("Unhandled exception")


@decorator
def send_typing_action(func, update, context, *args, **kwargs):
    """
    Send "Typing..." to the user while processing the request
    :param func: Function to decorate
    :type func: callable
    :type update: telegram.update.Update
    :type context: telegram.ext.callbackcontext.CallbackContext
    """
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    return func(update, context, *args, **kwargs)
