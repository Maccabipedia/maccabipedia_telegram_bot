import requests
from bs4 import BeautifulSoup

from maccabipediabot.maccabi_games_filtering import GamesFilter

_USER_DATE_GAMES_FILTER_KEY = "games_filter"
_MACCABIPEDIA_LINK = "www.maccabipedia.co.il"
_DONATION_PAGE_NAME = 'מכביפדיה:תרומות'


def transform_stats_to_pretty_hebrew_text(stats_summary):
    """
    Transform summary to pretty hebrew text
    :type stats_summary: dict
    :return: Hebrew text
    :rtype: str
    """
    return f"כמות נצחונות: {stats_summary['wins_count']} - ({stats_summary['wins_percentage']}%)" \
           f"\nכמות הפסדים: {stats_summary['losses_count']} - ({stats_summary['losses_percentage']}%)" \
           f"\nכמות תיקו: {stats_summary['ties_count']} - ({stats_summary['ties_percentage']}%)" \
           f"\nכמות משחקים ללא ספיגה: {stats_summary['clean_sheets_count']} - ({stats_summary['clean_sheets_percentage']}%)" \
           f"\n\n כמות שערים למכבי: {stats_summary['total_goals_for_maccabi']}" \
           f"\n כמות שערים נגד מכבי: {stats_summary['total_goals_against_maccabi']}" \
           f"\n יחס שערים למכבי חלקי נגד מכבי: {stats_summary['goals_ratio']}"


def set_default_filters_for_current_user(update, context):
    context.user_data[_USER_DATE_GAMES_FILTER_KEY] = GamesFilter()


def create_maccabipedia_shirt_number_category_html_text(shirt_number):
    return f"<a href='{_MACCABIPEDIA_LINK}/קטגוריה:שחקנים_שלבשו_מספר_{shirt_number}'>שחקנים שלבשו מספר {shirt_number}</a>"


def get_donation_link_html_text():
    return f"<a href='{_MACCABIPEDIA_LINK}/{_DONATION_PAGE_NAME}'>תרומה למכביפדיה</a>"


def get_song_lyrics(song_name):
    """
    scrapes the given song from it's page at maccabipedia, parsing the HTML to string and return the lyrics
    :param song_name: Tha name of the song
    :type song_name: str
    :return: link to the given song at maccabipedia & the lyrics of the given song
    :rtype: str
    """
    url = _MACCABIPEDIA_LINK + '/שיר:' + song_name
    response = requests.get('http://' + requests.utils.quote(url))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        lyrics = soup.find(class_='poem')
        return f"<a href='{url}' >שיר {song_name.replace('_', ' ')}:</a>\n{lyrics.text} \n\n"
    elif response.status_code == 404:
        return "לא נמצא שיר בשם זה. נסו שוב"
    else:
        return "אופס! קרתה שגיאה. נסו שוב עוד מספר דקות"


def transform_players_with_amount_to_telegram_html_text(top_players_with_amount):
    """
    Transforms the given list of players with amount (probably list of top players in a specific criteria, like top scorers)
    into html text that will be sent to the user (including links for players).
    :param top_players_with_amount: The players with the amount of the criteria
    :type top_players_with_amount: list of (str, int)
    :return: The top players as html text (With maccabipedia links to the players)
    :rtype: str
    """
    # The href="..." must have double quotation because we have some players with single quotation in their name
    telegram_html_text = "\n".join(f'<a href="{_MACCABIPEDIA_LINK}/{player_name}">{player_name}</a> : {amount}'
                                   for player_name, amount in top_players_with_amount)
    return telegram_html_text


def transform_players_with_maccabi_games_to_telegram_html_text(top_players_with_maccabi_games):
    """
    Transforms the given list of players with maccabi games (probably list of top players with specific streak, like winning streak)
    into html text that will be sent to the user (including links for players).
    :param top_players_with_maccabi_games: The players with the maccabi games
    :type top_players_with_maccabi_games: list of (str, maccabistats.stats.maccabi_games_stats.MaccabiGamesStats)
    :return: The top players as html text (With maccabipedia links to the players)
    :rtype: str
    """
    # The href="..." must have double quotation because we have some players with single quotation in their name
    telegram_html_text = "\n".join(f'<a href="{_MACCABIPEDIA_LINK}/{player_name}">{player_name}</a> : {maccabi_games.hebrew_representation}'
                                   for player_name, maccabi_games in top_players_with_maccabi_games)
    return telegram_html_text
