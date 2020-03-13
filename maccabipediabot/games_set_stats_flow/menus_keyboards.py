from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions, GamesStatsMainMenuOptions, PlayersStreaksStatsMenuOptions


def create_games_stats_main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("השחקנים המצטיינים", callback_data=GamesStatsMainMenuOptions.TOP_PLAYERS_STATS),
         InlineKeyboardButton("רצפי שחקנים", callback_data=GamesStatsMainMenuOptions.PLAYERS_STREAKS_STATS),
         InlineKeyboardButton("רצפי יריבות", callback_data=GamesStatsMainMenuOptions.TEAMS_STREAKS_STATS),
         InlineKeyboardButton('סיכום נתונים "יבשים"', callback_data=GamesStatsMainMenuOptions.SUMMARY_STATS)],

        [InlineKeyboardButton("סיים", callback_data=GamesStatsMainMenuOptions.FINISH)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_top_players_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("כובשים מובילים", callback_data=TopPlayersStatsMenuOptions.TOP_SCORERS),
         InlineKeyboardButton("מבשלים מובילים", callback_data=TopPlayersStatsMenuOptions.TOP_ASSISTERS),
         InlineKeyboardButton("שחקנים עם הכי הרבה הופעות", callback_data=TopPlayersStatsMenuOptions.MOST_PLAYED)],

    ]

    return InlineKeyboardMarkup(buttons)


def create_players_streaks_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("השחקן רק ניצח", callback_data=PlayersStreaksStatsMenuOptions.WINNING_STREAK),
         InlineKeyboardButton("השחקן לא הפסיד", callback_data=PlayersStreaksStatsMenuOptions.UNBEATEN_STREAK)],
    ]

    return InlineKeyboardMarkup(buttons)
