from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.games_set_stats_flow.menus_options import GamesStatsMainMenuOptions


def show_games_stats_main_menu(update, context):
    buttons = [
        [InlineKeyboardButton("כובשים מובילים", callback_data=GamesStatsMainMenuOptions.TOP_SCORERS),
         InlineKeyboardButton("מבשלים מובילים", callback_data=GamesStatsMainMenuOptions.TOP_ASSISTERS),
         InlineKeyboardButton("שחקנים עם הכי הרבה הופעות", callback_data=GamesStatsMainMenuOptions.MOST_PLAYED)],

        [InlineKeyboardButton("סיים", callback_data=GamesStatsMainMenuOptions.FINISH)]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="איזו סטטיסטיקה?", reply_markup=reply_markup)
