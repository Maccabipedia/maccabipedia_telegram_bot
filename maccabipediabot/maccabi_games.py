import logging

from maccabistats import load_from_maccabipedia_source
from maccabistats.data_improvement.naming_fixes import NamingErrorsFinder

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
    else:
        return very_similar_names


def get_similar_player_names(player_name):
    """
    :type player_name: str
    :rtype: list of str
    """
    very_similar_names = NamingErrorsFinder.get_similar_names(player_name, maccabipedia_games.available_players_names, ratio=0.9)
    if not very_similar_names:
        return NamingErrorsFinder.get_similar_names(player_name, maccabipedia_games.available_players_names, ratio=0.5)
    else:
        return very_similar_names
