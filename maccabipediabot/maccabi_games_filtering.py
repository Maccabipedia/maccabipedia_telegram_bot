import logging

from datetime import datetime
from maccabipediabot.maccabi_games import maccabipedia_games

from maccabipediabot.create_games_set_flow.menus_options import TeamFilteringMenuOptions, CompetitionFilteringMenuOptions, DateFilteringMenuOptions, \
    HomeAwayFilteringMenuOptions

logger = logging.getLogger(__name__)


class GamesFilter(object):
    ALL_COMPETITIONS = "all_competitions"
    ALL_TEAMS = "all_opponents"

    def __init__(self):
        """
        Initialize the games filter with the default filters ("No filter at all").
        """
        self.competition_name = self.ALL_COMPETITIONS
        self.team_name = self.ALL_TEAMS

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
        self.end_data = datetime.max

    def update_home_away_filter(self, home_away_filter):
        if home_away_filter == HomeAwayFilteringMenuOptions.AWAY:
            self.only_home_games = False
            self.only_away_games = True
        elif home_away_filter == HomeAwayFilteringMenuOptions.HOME:
            self.only_home_games = True
            self.only_away_games = False
        elif home_away_filter == HomeAwayFilteringMenuOptions.ALL_HOME_AWAY:
            self._set_default_home_away_filter()

    def update_competition_filter(self, competition_filter):
        if competition_filter == CompetitionFilteringMenuOptions.ALL_COMPETITIONS:
            self.competition_name = self.ALL_COMPETITIONS
        elif CompetitionFilteringMenuOptions.LEAGUE_ONLY:
            self.competition_name = "league_only"

    def update_team_filter_for_all_teams(self):
        self.team_name = self.ALL_TEAMS

    def update_team_filter(self, team_name):
        self.team_name = team_name

    def update_date_filter(self, date_filter):
        if date_filter == DateFilteringMenuOptions.SINCE_COUNTRY:
            self.start_date = "04.01.1949"
        elif date_filter == DateFilteringMenuOptions.ALL_TIME:
            self._set_default_date_filter()

    @property
    def team_filter_exists(self):
        return self.team_name != self.ALL_TEAMS

    @property
    def competition_filter_exists(self):
        return self.competition_name != self.ALL_COMPETITIONS

    @property
    def date_filter_exists(self):
        return self.start_date != datetime.min or self.end_data != datetime.max

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

    def filter_games(self):
        """
        Filter the games with the saved filter
        :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
        """
        filtered_games = maccabipedia_games
        logger.info(f"Unfiltered games: {filtered_games}")

        if self.games_filter.team_filter_exists:
            filtered_games = filtered_games.get_games_against_team(self.games_filter.team_name)
            logger.info(f"Filter: select games only against: {self.games_filter.team_name}. Games: {filtered_games}")

        # TODO: today we allow to filter ALL or LEAGUE_ONLY, that probably will be changed
        if self.games_filter.competition_filter_exists:
            filtered_games = filtered_games.league_games
            logger.info(f"Filter: select league games only. Games: {filtered_games}")

        if self.games_filter.date_filter_exists:
            filtered_games = filtered_games.played_after(self.games_filter.start_date).played_before(self.games_filter.end_data)
            logger.info(f"Filter: select games between {self.games_filter.start_date} <--> {self.games_filter.end_data}. Games: {filtered_games}")

        if self.games_filter.home_away_filter_exists:
            if self.games_filter.only_home_games:
                filtered_games = filtered_games.home_games
                logger.info(f"Filter: select only home games. Games: {filtered_games}")
            elif self.games_filter.only_away_games:
                filtered_games = filtered_games.away_games
                logger.info(f"Filter: select only away games. Games: {filtered_games}")

        return filtered_games