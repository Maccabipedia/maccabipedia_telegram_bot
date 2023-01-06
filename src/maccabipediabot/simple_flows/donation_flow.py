from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters

from common import get_donation_link_html_text
from handlers_utils import log_user_request, send_typing_action
from main_user_keyboard import MainKeyboardOptions


@log_user_request
@send_typing_action
def donation_handler(update, context):
    """
    Returns the donation page link from maccabipedia
    """

    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                             text=f"אנחנו מזמינים אתכם לתרום למכביפדיה.\n"
                                  f"לצורך המשך הפעילות, בשביל הוספה של תכנים חדשים ויכולות חדשות.\n"
                                  f"בכדי לתרום, היכנסו ל:\n"
                                  f"{get_donation_link_html_text()}")


def create_donation_handlers():
    """
    :rtype: CommandHandler, MessageHandler
    """
    donation_command_handler = CommandHandler("donate", donation_handler)
    donation_message_handler = MessageHandler(Filters.regex(f"^{MainKeyboardOptions.DONATE}$"), donation_handler)

    return donation_command_handler, donation_message_handler
