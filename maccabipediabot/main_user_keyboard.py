from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from maccabipediabot.emojis import MUSICAL_NOTE_EMOJI, HUMAN_RUNNING_EMOJI, MONEY_EMOJI, SHIRT_EMOJI, WRITE_EMOJI


class MainKeyboardOptions(object):
    GAMES_FILTERING = "סנן משחקים"
    GAMES_STATS = "סטטיסטיקה"
    SONG = f"שיר{MUSICAL_NOTE_EMOJI}"
    SEASON_STATS = "עונה"
    UNIFORMS = f"מדים{SHIRT_EMOJI}"
    DONATE = f"תרומה{MONEY_EMOJI}"
    PLAYER_STATS = f"שחקן{HUMAN_RUNNING_EMOJI}"
    FEEDBACK = f"כתבו לנו{WRITE_EMOJI}"

    GO_BACK = "חזור"


def show_the_user_main_keyboard_with_message(update, context):
    """
    Tells the user we go back to the main menu and show the ReplyKeyboard of the main menu
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=create_main_user_reply_keyboard(),
                             text=f"חוזרים לתפריט הראשי")


def create_go_back_reply_keyboard():
    buttons = [
        [KeyboardButton(MainKeyboardOptions.GO_BACK)]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard_reply_markup():
    return ReplyKeyboardRemove()


def create_main_user_reply_keyboard():
    buttons = [
        [KeyboardButton(MainKeyboardOptions.GAMES_STATS), KeyboardButton(MainKeyboardOptions.GAMES_FILTERING)],
        [KeyboardButton(MainKeyboardOptions.SONG), KeyboardButton(MainKeyboardOptions.PLAYER_STATS)],
        [KeyboardButton(MainKeyboardOptions.SEASON_STATS), KeyboardButton(MainKeyboardOptions.UNIFORMS)],

        [KeyboardButton(MainKeyboardOptions.DONATE), KeyboardButton(MainKeyboardOptions.FEEDBACK)]
    ]

    # We send this keyboard as one time keyboard, it will be collapsed
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
