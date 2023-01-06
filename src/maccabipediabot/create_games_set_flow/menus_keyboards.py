from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from create_games_set_flow.menus_options import GamesFilteringMainMenuOptions, HomeAwayFilteringMenuOptions, \
    TeamFilteringMenuOptions, CompetitionFilteringMenuOptions, DateFilteringMenuOptions, PlayedPlayerFilteringMenuOptions, \
    RefereeFilteringMenuOptions, StadiumFilteringMenuOptions, CoachFilteringMenuOptions, FinishOrContinueFilteringMenuOptions


def create_home_away_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("גם וגם", callback_data=HomeAwayFilteringMenuOptions.ALL_HOME_AWAY),
         InlineKeyboardButton("משחקי חוץ", callback_data=HomeAwayFilteringMenuOptions.AWAY),
         InlineKeyboardButton("משחקי בית", callback_data=HomeAwayFilteringMenuOptions.HOME)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_competition_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("ליגה", callback_data=CompetitionFilteringMenuOptions.LEAGUE_ONLY),
         InlineKeyboardButton("כל המפעלים", callback_data=CompetitionFilteringMenuOptions.ALL_COMPETITIONS)],

        [InlineKeyboardButton("גביע", callback_data=CompetitionFilteringMenuOptions.TROPHY_ONLY),
         InlineKeyboardButton("מפעלים אירופאים", callback_data=CompetitionFilteringMenuOptions.EUROPE_ONLY)]

    ]

    return InlineKeyboardMarkup(buttons)


def create_date_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("כל הזמן", callback_data=DateFilteringMenuOptions.ALL_TIME),
         InlineKeyboardButton("החל מקום המדינה", callback_data=DateFilteringMenuOptions.AFTER_COUNTRY_EXISTS),
         InlineKeyboardButton("לפני קום המדינה", callback_data=DateFilteringMenuOptions.BEFORE_COUNTRY_EXISTS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_team_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("קבוצה ספציפית", callback_data=TeamFilteringMenuOptions.SPECIFIC_TEAM),
         InlineKeyboardButton("כל הקבוצות", callback_data=TeamFilteringMenuOptions.ALL_TEAMS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_played_player_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("שחקן ספציפי", callback_data=PlayedPlayerFilteringMenuOptions.SPECIFIC_PLAYER),
         InlineKeyboardButton("כל השחקנים", callback_data=PlayedPlayerFilteringMenuOptions.ALL_PLAYERS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_referee_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("שופט ספציפי", callback_data=RefereeFilteringMenuOptions.SPECIFIC_REFEREE),
         InlineKeyboardButton("כל השופטים", callback_data=RefereeFilteringMenuOptions.ALL_REFEREES)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_stadium_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("אצטדיון ספציפי", callback_data=StadiumFilteringMenuOptions.SPECIFIC_STADIUM),
         InlineKeyboardButton("כל האצטדיונים", callback_data=StadiumFilteringMenuOptions.ALL_STADIUMS)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_coach_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("מאמן ספציפי", callback_data=CoachFilteringMenuOptions.SPECIFIC_COACH),
         InlineKeyboardButton("כל המאמנים", callback_data=CoachFilteringMenuOptions.ALL_COACHES)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_finish_or_continue_games_filter_menu():
    buttons = [
        [InlineKeyboardButton("סנן משחקים", callback_data=FinishOrContinueFilteringMenuOptions.CONTINUE),
         InlineKeyboardButton("סיים", callback_data=FinishOrContinueFilteringMenuOptions.FINISH)]
    ]

    return InlineKeyboardMarkup(buttons)


def create_games_filter_main_menu(first_time_menu):
    buttons = [
        [InlineKeyboardButton("ביתיות", callback_data=GamesFilteringMainMenuOptions.HOME_AWAY),
         InlineKeyboardButton("מפעל", callback_data=GamesFilteringMainMenuOptions.COMPETITION),
         InlineKeyboardButton("מאמן", callback_data=GamesFilteringMainMenuOptions.COACH),
         InlineKeyboardButton("תאריך", callback_data=GamesFilteringMainMenuOptions.DATE)
         # We cant use it now because we dont treat some stadiums name as the same one like: בלומפילד, אצטדיון בלמפילד, באסה
         # InlineKeyboardButton("אצטדיון", callback_data=GamesFilteringMainMenuOptions.STADIUM),
         ],

        [InlineKeyboardButton("יריבה", callback_data=GamesFilteringMainMenuOptions.TEAM),
         InlineKeyboardButton("שחקן ששיחק", callback_data=GamesFilteringMainMenuOptions.PLAYED_PLAYER),
         InlineKeyboardButton("שופט", callback_data=GamesFilteringMainMenuOptions.REFEREE)]

    ]

    finish_button_text = "בחר את כל המשחקים" if first_time_menu else "סיים"
    buttons.append([InlineKeyboardButton(finish_button_text, callback_data=GamesFilteringMainMenuOptions.FINISH)])

    return InlineKeyboardMarkup(buttons)
