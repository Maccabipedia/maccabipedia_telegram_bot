from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.create_games_set_flow.menus_options import GamesFilteringMainMenuOptions, HomeAwayFilteringMenuOptions, TeamFilteringMenuOptions, \
    CompetitionFilteringMenuOptions, DateFilteringMenuOptions


def create_home_away_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("משחקי בית", callback_data=HomeAwayFilteringMenuOptions.HOME),
         InlineKeyboardButton("משחקי חוץ", callback_data=HomeAwayFilteringMenuOptions.AWAY),
         InlineKeyboardButton("גם וגם", callback_data=HomeAwayFilteringMenuOptions.ALL_HOME_AWAY)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_competition_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("ליגה", callback_data=CompetitionFilteringMenuOptions.LEAGUE_ONLY),
         InlineKeyboardButton("כל המסגרות", callback_data=CompetitionFilteringMenuOptions.ALL_COMPETITIONS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_date_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("החל מקום המדינה", callback_data=DateFilteringMenuOptions.SINCE_COUNTRY),
         InlineKeyboardButton("כל הזמן", callback_data=DateFilteringMenuOptions.ALL_TIME)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_team_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("קבוצה ספציפית", callback_data=TeamFilteringMenuOptions.SPECIFIC_TEAM),
         InlineKeyboardButton("כל הקבוצות", callback_data=TeamFilteringMenuOptions.ALL_TEAMS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_games_filter_main_menu(first_time_menu):
    buttons = [
        [InlineKeyboardButton("ביתיות", callback_data=GamesFilteringMainMenuOptions.HOME_AWAY),
         InlineKeyboardButton("מפעל", callback_data=GamesFilteringMainMenuOptions.COMPETITION),
         InlineKeyboardButton("יריבה", callback_data=GamesFilteringMainMenuOptions.TEAM),
         InlineKeyboardButton("תאריך", callback_data=GamesFilteringMainMenuOptions.DATE)],

    ]

    finish_button_text = "בחר את כל המשחקים" if first_time_menu else "סיים"
    buttons.append([InlineKeyboardButton(finish_button_text, callback_data=GamesFilteringMainMenuOptions.FINISH)])

    return InlineKeyboardMarkup(buttons)
