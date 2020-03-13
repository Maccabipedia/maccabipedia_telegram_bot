import logging

from maccabistats import load_from_maccabipedia_source
from maccabistats.data_improvement.naming_fixes import NamingErrorsFinder

from maccabipediabot.create_games_set_flow.menus_options import TeamFilteringMenuOptions, CompetitionFilteringMenuOptions, DateFilteringMenuOptions, \
    HomeAwayFilteringMenuOptions

logger = logging.getLogger(__name__)

maccabipedia_games = load_from_maccabipedia_source()


def get_similar_teams_names(team_name):
    """
    :type team_name: str
    :rtype: list of str
    """
    very_similar_names = NamingErrorsFinder.get_similar_names(team_name, maccabipedia_games.available_opponents, ratio=0.9)
    if not very_similar_names:
        return NamingErrorsFinder.get_similar_names(team_name, maccabipedia_games.available_opponents, ratio=0.5)


def get_games_by_filters(user_data_filters):
    """
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """
    filtered_games = maccabipedia_games

    logger.info(f"unfiltered games: {filtered_games}")
    # TODO - save the filter and result in different values (like, specific team and which team name user choose)
    team_filter = user_data_filters['team']
    if team_filter != TeamFilteringMenuOptions.ALL_TEAMS:
        filtered_games = filtered_games.get_games_against_team(team_filter)
        logger.info(f"Filter team with {team_filter} - {filtered_games}")

    competition_filter = user_data_filters['competition']
    if competition_filter == CompetitionFilteringMenuOptions.LEAGUE_ONLY:
        filtered_games = filtered_games.league_games
        logger.info(f"Filter competition with league only - {filtered_games}")

    date_filter = user_data_filters['date']
    if date_filter == DateFilteringMenuOptions.SINCE_COUNTRY:
        filtered_games = filtered_games.played_after("04.01.1949")
        logger.info(f"Filter with games after country exists - {filtered_games}")

    home_away_filter = user_data_filters['home_away']
    if home_away_filter == HomeAwayFilteringMenuOptions.AWAY:
        filtered_games = filtered_games.home_games
        logger.info(f"Filter only home games - {filtered_games}")
    elif home_away_filter == HomeAwayFilteringMenuOptions.AWAY:
        filtered_games = filtered_games.away_games
        logger.info(f"Filter only away games - {filtered_games}")

    return filtered_games
