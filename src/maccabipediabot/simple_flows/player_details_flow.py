from telegram import ParseMode
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from common import get_profile
from handlers_utils import log_user_request, send_typing_action, go_back_to_main_menu_from_conversation_handler
from main_user_keyboard import MainKeyboardOptions, create_main_user_reply_keyboard, create_go_back_reply_keyboard

_show_player_details_state = range(1)


@log_user_request
@send_typing_action
def show_profile_details_handler(update, context):
    """
    handle profiles of players. Will be extended to all staff people later
    :return: parsed profile data of the given player
    """
    player_name = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=get_profile(player_name),
                             reply_markup=create_main_user_reply_keyboard())

    return ConversationHandler.END


@log_user_request
@send_typing_action
def player_details_entry_point(update, context):
    """
    The entry point of show player details process, we ask the player name from the user
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_go_back_reply_keyboard(),
                             text=f"הקלד את השחקן שעבורו תרצה לקבל את המידע:")

    return _show_player_details_state


def create_player_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("player", player_details_entry_point),
                      MessageHandler(Filters.regex(f"^{MainKeyboardOptions.PLAYER_STATS}$"), player_details_entry_point)],
        states={_show_player_details_state: [
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler),
            MessageHandler(Filters.text, show_profile_details_handler)]},
        fallbacks=[
            MessageHandler(Filters.regex(f"^{MainKeyboardOptions.GO_BACK}$"), go_back_to_main_menu_from_conversation_handler)]
    )
