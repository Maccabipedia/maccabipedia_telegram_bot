class TeamFilteringMenuOptions(object):
    MENU_NAME = "team_filtering_menu"
    ALL_TEAMS = f"{MENU_NAME}_all_teams"
    SPECIFIC_TEAM = f"{MENU_NAME}_specific_team"


class CompetitionFilteringMenuOptions(object):
    MENU_NAME = "competition_filtering_menu"
    ALL_COMPETITIONS = f"{MENU_NAME}_all_competitions"
    LEAGUE_ONLY = f"{MENU_NAME}_league_only"


class DateFilteringMenuOptions(object):
    MENU_NAME = "date_filtering_menu"
    ALL_TIME = f"{MENU_NAME}_all"
    SINCE_COUNTRY = f"{MENU_NAME}_country"


class HomeAwayFilteringMenuOptions(object):
    MENU_NAME = "home_away_filtering_menu"
    HOME = f"{MENU_NAME}_home"
    AWAY = f"{MENU_NAME}_away"
    ALL_HOME_AWAY = f"{MENU_NAME}_all"


class GamesFilteringMainMenuOptions(object):
    MENU_NAME = "games_filtering_main_menu"
    HOME_AWAY = f"{MENU_NAME}_home_away"
    TEAM = f"{MENU_NAME}_team"
    COMPETITION = f"{MENU_NAME}_competition"
    DATE = f"{MENU_NAME}_date"
    FINISH = f"{MENU_NAME}_finish"
