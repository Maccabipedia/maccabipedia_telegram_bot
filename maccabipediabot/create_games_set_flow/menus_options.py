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


class RefereeFilteringMenuOptions(object):
    MENU_NAME = "referee_filtering_menu"
    ALL_REFEREES = f"{MENU_NAME}_all_referees"
    SPECIFIC_REFEREE = f"{MENU_NAME}_specific_referee"

    TEXT = "סנן לפי שופט:"


class StadiumFilteringMenuOptions(object):
    MENU_NAME = "stadium_filtering_menu"
    ALL_STADIUMS = f"{MENU_NAME}_all_stadiums"
    SPECIFIC_STADIUM = f"{MENU_NAME}_specific_stadium"

    TEXT = "סנן לפי אצטדיון:"


class CoachFilteringMenuOptions(object):
    MENU_NAME = "coach_filtering_menu"
    ALL_COACHES = f"{MENU_NAME}_all_coaches"
    SPECIFIC_COACH = f"{MENU_NAME}_specific_coach"

    TEXT = "סנן לפי מאמן:"


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
    REFEREE = f"{MENU_NAME}_referee"
    STADIUM = f"{MENU_NAME}_stadium"
    COACH = f"{MENU_NAME}_coach"
    FINISH = f"{MENU_NAME}_finish"

    FIRST_TIME_TEXT = "סנן משחקים לפי:"
    AFTER_FIRST_TIME_TEXT = "סנן משחקים נוספים, או סיים:"
