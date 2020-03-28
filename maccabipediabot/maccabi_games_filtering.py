import logging
from datetime import datetime

from maccabipediabot.create_games_set_flow.menus_options import CompetitionFilteringMenuOptions, DateFilteringMenuOptions, \
    HomeAwayFilteringMenuOptions
from maccabipediabot.maccabi_games import get_maccabipedia_games

logger = logging.getLogger(__name__)


class GamesFilter(object):
    ALL_TEAMS = "all_opponents"
    ALL_PLAYERS = "all_players"
    ALL_REFEREES = "all_referees"
    ALL_STADIUMS = "all_stadiums"
    ALL_COACHES = "all_coaches"

    ALL_COMPETITIONS = "all_competitions"
    LEAGUE_CATEGORY = "ליגה"
    TROPHY_CATEGORY = "גביע"
    EUROPE_CATEGORY = "מפעלים אירופאים"
    LEAGUE_COMPETITIONS = ["ליגת העל", "ליגה לאומית", "ליגת Winner", "ליגת הבורסה לניירות ערך", "ליגה א'", "ליגה א"]
    TROPHY_COMPETITIONS = ["הגביע הארץ ישראלי", "גביע המלחמה", "גביע המדינה"]
    EUROPE_COMPETITIONS = ["הליגה האירופית", "גביע אסיה לאלופות", "מוקדמות הליגה האירופית", "ליגת האלופות", "גביע אופא",
                           "פלייאוף הליגה האירופית", "גביע אירופה למחזיקות גביע", "גביע האינטרטוטו", "מוקדמות ליגת האלופות"]

    ALL_DATES = "all_dates"
    AFTER_COUNTRY = "החל מקום המדינה"
    BEFORE_COUNTRY = "לפני קום המדינה"

    def __init__(self):
        """
        Initialize the games filter with the default filters ("No filter at all").
        """
        self.competition_category = self.ALL_COMPETITIONS
        self.competitions_name = self.ALL_COMPETITIONS
        self.team_name = self.ALL_TEAMS
        self.played_player = self.ALL_PLAYERS
        self.referee_name = self.ALL_REFEREES
        self.stadium_name = self.ALL_STADIUMS
        self.coach_name = self.ALL_COACHES

        self._set_default_home_away_filter()
        self._set_default_date_filter()

    def _set_default_home_away_filter(self):
        """
        Initialize the home_away filter to include all games
        """
        self.only_home_games = False
        self.only_away_games = False

    def _set_default_date_filter(self):
        """
        Initialize the date filter to include all time
        """
        self.start_date = datetime.min
        self.end_date = datetime.max
        self.date_category = self.ALL_DATES

    def update_home_away_filter(self, home_away_filter):
        if home_away_filter == HomeAwayFilteringMenuOptions.AWAY:
            self.only_home_games = False
            self.only_away_games = True
        elif home_away_filter == HomeAwayFilteringMenuOptions.HOME:
            self.only_home_games = True
            self.only_away_games = False
        elif home_away_filter == HomeAwayFilteringMenuOptions.ALL_HOME_AWAY:
            self._set_default_home_away_filter()
        else:
            raise TypeError(f"Unknown home_away filter: {home_away_filter}")

    def update_competition_filter(self, competition_filter):
        if competition_filter == CompetitionFilteringMenuOptions.ALL_COMPETITIONS:
            self.competitions_name = self.ALL_COMPETITIONS
            self.competition_category = self.ALL_COMPETITIONS
        elif competition_filter == CompetitionFilteringMenuOptions.LEAGUE_ONLY:
            self.competitions_name = self.LEAGUE_COMPETITIONS
            self.competition_category = self.LEAGUE_CATEGORY
        elif competition_filter == CompetitionFilteringMenuOptions.TROPHY_ONLY:
            self.competitions_name = self.TROPHY_COMPETITIONS
            self.competition_category = self.TROPHY_CATEGORY
        elif competition_filter == CompetitionFilteringMenuOptions.EUROPE_ONLY:
            self.competitions_name = self.EUROPE_COMPETITIONS
            self.competition_category = self.EUROPE_CATEGORY
        else:
            raise TypeError(f"Unknown competition filter: {competition_filter}")

    def update_team_filter_for_all_teams(self):
        self.team_name = self.ALL_TEAMS

    def update_team_filter(self, team_name):
        self.team_name = team_name

    def update_player_filter_to_all_players(self):
        self.played_player = self.ALL_PLAYERS

    def update_played_player_filter(self, player_name):
        self.played_player = player_name

    def update_referee_filter_to_all_referees(self):
        self.referee_name = self.ALL_REFEREES

    def update_referee_filter(self, referee_name):
        self.referee_name = referee_name

    def update_stadium_filter_to_all_stadiums(self):
        self.stadium_name = self.ALL_STADIUMS

    def update_stadium_filter(self, stadium_name):
        self.stadium_name = stadium_name

    def update_coach_filter_to_all_coaches(self):
        self.coach_name = self.ALL_COACHES

    def update_coach_filter(self, coach_name):
        self.coach_name = coach_name

    def update_date_filter(self, date_filter):
        if date_filter == DateFilteringMenuOptions.AFTER_COUNTRY_EXISTS:
            self._set_default_date_filter()
            self.start_date = "04.01.1949"
            self.date_category = self.AFTER_COUNTRY
        elif date_filter == DateFilteringMenuOptions.BEFORE_COUNTRY_EXISTS:
            self._set_default_date_filter()
            self.end_date = "04.01.1949"
            self.date_category = self.BEFORE_COUNTRY
        elif date_filter == DateFilteringMenuOptions.ALL_TIME:
            self._set_default_date_filter()
        else:
            raise TypeError(f"Unknown date filter: {date_filter}")

    @property
    def coach_filter_exists(self):
        return self.coach_name != self.ALL_COACHES

    @property
    def stadium_filter_exists(self):
        return self.stadium_name != self.ALL_STADIUMS

    @property
    def referee_filter_exists(self):
        return self.referee_name != self.ALL_REFEREES

    @property
    def team_filter_exists(self):
        return self.team_name != self.ALL_TEAMS

    @property
    def played_player_filter_exists(self):
        return self.played_player != self.ALL_PLAYERS

    @property
    def competition_filter_exists(self):
        return self.competitions_name != self.ALL_COMPETITIONS

    @property
    def date_filter_exists(self):
        return self.start_date != datetime.min or self.end_date != datetime.max

    @property
    def home_away_filter_exists(self):
        return self.only_away_games or self.only_home_games


class MaccabiGamesFiltering(object):
    def __init__(self, games_filter):
        """
        :param games_filter: The filter to use to select which games wil lbe in the group
        :type games_filter: GamesFilter
        """
        self.games_filter = games_filter

    def to_user_description(self):
        """
        Returns a description of the filtering that will be shown to the user
        :rtype: str
        """
        descriptions = []
        if self.games_filter.home_away_filter_exists:
            where = "בית" if self.games_filter.only_home_games else "חוץ"
            descriptions.append(f"משחקי {where}")
        if self.games_filter.date_filter_exists:
            descriptions.append(f"ששוחקו {self.games_filter.date_category}")
        if self.games_filter.competition_filter_exists:
            descriptions.append(f"ששוחקו ב{self.games_filter.competition_category}")
        if self.games_filter.team_filter_exists:
            descriptions.append(f"נגד {self.games_filter.team_name}")
        if self.games_filter.stadium_filter_exists:
            descriptions.append(f"ששוחקו ב {self.games_filter.stadium_name}")
        if self.games_filter.played_player_filter_exists:
            descriptions.append(f"שהשחקן {self.games_filter.played_player} שיחק")
        if self.games_filter.coach_filter_exists:
            descriptions.append(f"ש{self.games_filter.coach_name} אימן")
        if self.games_filter.referee_filter_exists:
            descriptions.append(f"שהשופט{self.games_filter.referee_name} שפט")

        if descriptions:
            return "\n".join(descriptions)
        else:
            return "כל המשחקים האפשריים"

    def filter_games(self):
        """
        Filter the games with the saved filter
        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        filtered_games = get_maccabipedia_games()
        logger.info(f"Unfiltered games: {filtered_games}")

        if self.games_filter.team_filter_exists:
            filtered_games = filtered_games.get_games_against_team(self.games_filter.team_name)
            logger.info(f"Filter: select games only against: {self.games_filter.team_name}. Games: {filtered_games}")

        if self.games_filter.played_player_filter_exists:
            filtered_games = filtered_games.get_games_by_played_player_name(self.games_filter.played_player)
            logger.info(f"Filter: select games with this player only: {self.games_filter.played_player}. Games: {filtered_games}")

        if self.games_filter.referee_filter_exists:
            filtered_games = filtered_games.get_games_by_referee(self.games_filter.referee_name)
            logger.info(f"Filter: select games with this referee only: {self.games_filter.referee_name}. Games: {filtered_games}")

        if self.games_filter.stadium_filter_exists:
            filtered_games = filtered_games.get_games_by_stadium(self.games_filter.stadium_name)
            logger.info(f"Filter: select games which played at stadium: {self.games_filter.stadium_name}. Games: {filtered_games}")

        if self.games_filter.coach_filter_exists:
            filtered_games = filtered_games.get_games_by_coach(self.games_filter.coach_name)
            logger.info(f"Filter: select games with maccabi coach: {self.games_filter.coach_name}. Games: {filtered_games}")

        if self.games_filter.competition_filter_exists:
            filtered_games = filtered_games.get_games_by_competition(self.games_filter.competitions_name)
            logger.info(f"Filter: select these competitions only: {self.games_filter.competitions_name}. Games: {filtered_games}")

        if self.games_filter.date_filter_exists:
            filtered_games = filtered_games.played_after(self.games_filter.start_date).played_before(self.games_filter.end_date)
            logger.info(f"Filter: select games between {self.games_filter.start_date} <--> {self.games_filter.end_date}. Games: {filtered_games}")

        if self.games_filter.home_away_filter_exists:
            if self.games_filter.only_home_games:
                filtered_games = filtered_games.home_games
                logger.info(f"Filter: select only home games. Games: {filtered_games}")
            elif self.games_filter.only_away_games:
                filtered_games = filtered_games.away_games
                logger.info(f"Filter: select only away games. Games: {filtered_games}")

        return filtered_games
