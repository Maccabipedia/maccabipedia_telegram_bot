import logging

from maccabistats import load_from_maccabipedia_source
from maccabistats.data_improvement.naming_fixes import NamingErrorsFinder

logger = logging.getLogger(__name__)

maccabipedia_games = load_from_maccabipedia_source()


def _get_similar_names(main_name, possible_similar_names):
    """
    Checking what are the similar names from possible names to the main_name.
    :type main_name: str
    :type possible_similar_names: list of str
    :rtype: list of str
    """
    very_similar_names = NamingErrorsFinder.get_similar_names(main_name, possible_similar_names, ratio=0.9)
    if not very_similar_names:
        return NamingErrorsFinder.get_similar_names(main_name, possible_similar_names, ratio=0.5)
    else:
        return very_similar_names


def get_similar_teams_names(team_name):
    """
    :type team_name: str
    :rtype: list of str
    """
    return _get_similar_names(team_name, maccabipedia_games.available_opponents)


def get_similar_player_names(player_name):
    """
    :type player_name: str
    :rtype: list of str
    """
    return _get_similar_names(player_name, maccabipedia_games.available_players_names)


def get_similar_referees_names(referee_name):
    """
    :type referee_name: str
    :rtype: list of str
    """
    return _get_similar_names(referee_name, maccabipedia_games.available_referees)


def get_similar_stadiums_names(stadium_name):
    """
    :type stadium_name: str
    :rtype: list of str
    """
    return _get_similar_names(stadium_name, maccabipedia_games.available_stadiums)


def get_similar_coaches_names(coach_name):
    """
    :type coach_name: str
    :rtype: list of str
    """
    return _get_similar_names(coach_name, maccabipedia_games.available_coaches)
