from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.emojis import SOCCER_BALL_EMOJI, FORK_AND_KNIFE_EMOJI, LETTER_C_EMOJI
from maccabipediabot.games_set_stats_flow.menus_options import TopPlayersStatsMenuOptions, GamesStatsMainMenuOptions, PlayersStreaksStatsMenuOptions, \
    MoreStatsOrFinishMenuOptions, TeamStreaksStatsMenuOptions


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
        [InlineKeyboardButton("סטטיסטיקה נוספת", callback_data=MoreStatsOrFinishMenuOptions.MORE_STATS),
         InlineKeyboardButton("סיים", callback_data=MoreStatsOrFinishMenuOptions.FINISH)],

    ]

    return InlineKeyboardMarkup(buttons)


def create_top_players_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton(f"כובשים מובילים{SOCCER_BALL_EMOJI}", callback_data=TopPlayersStatsMenuOptions.TOP_SCORERS),
         InlineKeyboardButton(f"מבשלים מובילים{FORK_AND_KNIFE_EMOJI}", callback_data=TopPlayersStatsMenuOptions.TOP_ASSISTERS)],

        [InlineKeyboardButton("הכי הרבה הופעות", callback_data=TopPlayersStatsMenuOptions.MOST_PLAYED),
         InlineKeyboardButton(f"קפטנים מובילים{LETTER_C_EMOJI}", callback_data=TopPlayersStatsMenuOptions.MOST_CAPTAIN)],

    ]

    return InlineKeyboardMarkup(buttons)


def create_players_streaks_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("השחקן רק ניצח", callback_data=PlayersStreaksStatsMenuOptions.WINNING_STREAK),
         InlineKeyboardButton("השחקן לא הפסיד", callback_data=PlayersStreaksStatsMenuOptions.UNBEATEN_STREAK)],

        [InlineKeyboardButton("מכבי הבקיעה", callback_data=PlayersStreaksStatsMenuOptions.SCORE_AT_LEAST_A_GOAL),
         InlineKeyboardButton("מכבי לא ספגה", callback_data=PlayersStreaksStatsMenuOptions.CLEAN_SHEETS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_teams_streaks_games_stats_keyboard():
    buttons = [
        [InlineKeyboardButton("מכבי רק ניצחה", callback_data=TeamStreaksStatsMenuOptions.WINNING_STREAK),
         InlineKeyboardButton("מכבי לא הפסידה", callback_data=TeamStreaksStatsMenuOptions.UNBEATEN_STREAK)],

        [InlineKeyboardButton("מכבי הבקיעה", callback_data=TeamStreaksStatsMenuOptions.SCORE_AT_LEAST_A_GOAL),
         InlineKeyboardButton("מכבי לא ספגה", callback_data=TeamStreaksStatsMenuOptions.CLEAN_SHEETS)]
    ]

    return InlineKeyboardMarkup(buttons)
