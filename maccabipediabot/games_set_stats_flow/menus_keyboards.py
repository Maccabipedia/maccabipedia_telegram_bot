from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions, GamesStatsMainMenuOptions, PlayersStreaksStatsMenuOptions, \
    MoreStatsOrFinishMenuOptions


def create_games_stats_main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("השחקנים המצטיינים", callback_data=GamesStatsMainMenuOptions.TOP_PLAYERS_STATS),
         InlineKeyboardButton('פילוח תוצאות', callback_data=GamesStatsMainMenuOptions.SUMMARY_STATS)],

        [InlineKeyboardButton("רצפי שחקנים", callback_data=GamesStatsMainMenuOptions.PLAYERS_STREAKS_STATS),
         InlineKeyboardButton("רצפי יריבות", callback_data=GamesStatsMainMenuOptions.TEAMS_STREAKS_STATS)],

        [InlineKeyboardButton("סיים", callback_data=GamesStatsMainMenuOptions.FINISH)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_more_stats_or_finish_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("סטטיסטיקות נוספות", callback_data=MoreStatsOrFinishMenuOptions.MORE_STATS),
         InlineKeyboardButton("סיים", callback_data=MoreStatsOrFinishMenuOptions.FINISH)],

    ]

    return InlineKeyboardMarkup(buttons)


def create_top_players_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("⚽כובשים מובילים", callback_data=TopPlayersStatsMenuOptions.TOP_SCORERS),
         InlineKeyboardButton("🍴מבשלים מובילים", callback_data=TopPlayersStatsMenuOptions.TOP_ASSISTERS)],

        [InlineKeyboardButton("הכי הרבה הופעות", callback_data=TopPlayersStatsMenuOptions.MOST_PLAYED),
         InlineKeyboardButton("קפטנים מובילים", callback_data=TopPlayersStatsMenuOptions.MOST_CAPTAIN)],

    ]

    return InlineKeyboardMarkup(buttons)


def create_players_streaks_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("השחקן רק ניצח", callback_data=PlayersStreaksStatsMenuOptions.WINNING_STREAK),
         InlineKeyboardButton("השחקן לא הפסיד", callback_data=PlayersStreaksStatsMenuOptions.UNBEATEN_STREAK)],
    ]

    return InlineKeyboardMarkup(buttons)
