from maccabipediabot.create_games_set_flow.games_set_conversation_handler_states import games_filtering
from maccabipediabot.create_games_set_flow.menus_keyboards import create_games_filter_main_menu
from maccabipediabot.create_games_set_flow.menus_options import GamesFilteringMainMenuOptions


def get_button_text_from_query_data(query):
    from itertools import chain

    return next(button.text for button in chain.from_iterable(query.message.reply_markup.inline_keyboard) if
                button.callback_data == query.data)


def go_back_to_main_games_filter_menu(update, context):
    reply_keyboard = create_games_filter_main_menu(first_time_menu=False)

    # This is not the first time the user sees the games filtering menu, we will ask him if he want to continue filtering or to finish the process.
    context.bot.send_message(chat_id=update.effective_chat.id, text=GamesFilteringMainMenuOptions.AFTER_FIRST_TIME_TEXT, reply_markup=reply_keyboard)
    return games_filtering
