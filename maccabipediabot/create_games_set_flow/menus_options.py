class TeamFilteringMenuOptions(object):
    MENU_NAME = "team_filtering_menu"
    ALL_TEAMS = f"{MENU_NAME}_all_teams"
    SPECIFIC_TEAM = f"{MENU_NAME}_specific_team"

    TEXT = "סנן לפי יריבות:"


class PlayedPlayerFilteringMenuOptions(object):
    MENU_NAME = "played_player_filtering_menu"
    ALL_PLAYERS = f"{MENU_NAME}_all_players"
    SPECIFIC_PLAYER = f"{MENU_NAME}_specific_player"

    TEXT = "סנן לפי שחקן:"


class CompetitionFilteringMenuOptions(object):
    MENU_NAME = "competition_filtering_menu"
    ALL_COMPETITIONS = f"{MENU_NAME}_all_competitions"
    LEAGUE_ONLY = f"{MENU_NAME}_league_only"

    TEXT = "סנן לפי מפעל:"


class DateFilteringMenuOptions(object):
    MENU_NAME = "date_filtering_menu"
    ALL_TIME = f"{MENU_NAME}_all"
    SINCE_COUNTRY = f"{MENU_NAME}_country"

    TEXT = "סנן לפי תאריכי משחקים:"


class HomeAwayFilteringMenuOptions(object):
    MENU_NAME = "home_away_filtering_menu"
    HOME = f"{MENU_NAME}_home"
    AWAY = f"{MENU_NAME}_away"
    ALL_HOME_AWAY = f"{MENU_NAME}_all"

    TEXT = "סנן משחקים לפי ביתיות:"


class GamesFilteringMainMenuOptions(object):
    MENU_NAME = "games_filtering_main_menu"
    HOME_AWAY = f"{MENU_NAME}_home_away"
    TEAM = f"{MENU_NAME}_team"
    COMPETITION = f"{MENU_NAME}_competition"
    DATE = f"{MENU_NAME}_date"
    PLAYED_PLAYER = f"{MENU_NAME}_played_player"
    FINISH = f"{MENU_NAME}_finish"

    FIRST_TIME_TEXT = "סנן משחקים לפי:"
    AFTER_FIRST_TIME_TEXT = "סנן משחקים נוספים, או סיים:"
