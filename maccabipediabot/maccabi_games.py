import logging
import tempfile
import urllib.request
from pathlib import Path

from maccabistats import get_maccabi_stats_as_newest_wrapper
from maccabistats.data_improvement.naming_fixes import NamingErrorsFinder

logger = logging.getLogger(__name__)
_maccabipedia_games = None


def get_maccabipedia_games():
    """
    :rtype: maccabistats.stats.maccabi_games_stats.MaccabiGamesStats
    """
    global _maccabipedia_games
    if _maccabipedia_games is None:
        download_maccabipedia_games_for_heroku()

    return _maccabipedia_games


def download_maccabipedia_games_for_heroku():
    """
    In order to run maccabipedia telegram bot we need to use the filesystem (to load the maccabipedia games).
    Heroku filesystem support is not so good, so we did some hacks like downloading the games from our website
    (we should improve this to change the games we download without code change).
    """
    with tempfile.TemporaryDirectory() as temp_maccabipedia_games_folder:
        maccabipedia_games_file_path = Path(temp_maccabipedia_games_folder) / "MaccabiPedia.games"

        logger.info(f"Downloading maccabipedia games do: {maccabipedia_games_file_path}")
        urllib.request.urlretrieve("http://maccabipedia.co.il/MaccabiPedia-2.9.1-2020-03-15%2002-17-03.games", maccabipedia_games_file_path)

        global _maccabipedia_games
        _maccabipedia_games = get_maccabi_stats_as_newest_wrapper(maccabipedia_games_file_path)
        logger.info(f"Loading maccabipedia games (as newest wrapper) from: {maccabipedia_games_file_path}")


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
    return _get_similar_names(team_name, get_maccabipedia_games().available_opponents)


def get_similar_player_names(player_name):
    """
    :type player_name: str
    :rtype: list of str
    """
    return _get_similar_names(player_name, get_maccabipedia_games().available_players_names)


def get_similar_referees_names(referee_name):
    """
    :type referee_name: str
    :rtype: list of str
    """
    return _get_similar_names(referee_name, get_maccabipedia_games().available_referees)


def get_similar_stadiums_names(stadium_name):
    """
    :type stadium_name: str
    :rtype: list of str
    """
    return _get_similar_names(stadium_name, get_maccabipedia_games().available_stadiums)


def get_similar_coaches_names(coach_name):
    """
    :type coach_name: str
    :rtype: list of str
    """
    return _get_similar_names(coach_name, get_maccabipedia_games().available_coaches)
