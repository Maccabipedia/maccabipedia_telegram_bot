import logging
import datetime

import requests
from bs4 import BeautifulSoup

from maccabipediabot.consts import _MACCABIPEDIA_LINK, _DONATION_PAGE_NAME
from maccabipediabot.maccabi_games_filtering import GamesFilter

_USER_DATE_GAMES_FILTER_KEY = "games_filter"


logger = logging.getLogger(__name__)


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
           f"\n יחס שערים (מכבי/יריבה): {stats_summary['goals_ratio']}"


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


def get_current_season():
    """
    return the current season according to the current date (assuming new seasons start at august)
    :return current season in format 2000/01
    :rtype str
    """
    today = datetime.datetime.now()
    if today.month < 8:
        return f"{str(today.year - 1)}/{str(today.year)[2:]}"
    else:
        return f"{str(today.year)}/{str(today.year - 1)[2:]}"


def format_season_id(season):
    """
    Format the given season to the canonical season format, Handling these formats:
    1995-96, 1995/96, 95-96, 95/96, 1996, 96
    Return the input if could not find matching format.
    :param season: The season to find a match for
    :type season: str
    :return: The formatted season string or the input if could not find matching format
    :rtype: str
    """
    if season in ["נוכחית", "הנוכחית", "אחרונה", "האחרונה"]:
        return get_current_season()

    # Avoid non numbers cases (for the two possible separators) and non valid formats
    if not season.split('-')[0].split('/')[0].isdigit():
        return season  # Nothing to do with this format

    season = season.replace('-', '/')  # Replacing '-' with '/' to get correct format

    if len(season) == 9 or len(season) == 7 or len(season) == 5:
        if '/' not in season:
            return season  # Nothing to do with this format

    if len(season) == 9:  # Long format --> 1995/1996
        years = season.split('/')
        return f"{years[0]}/{years[1][2:]}"

    if len(season) == 7:  # Normal format --> 1995/96
        return season
    elif len(season) == 5:  # Short format --> 95/96
        prefix = "20" if int(season[0:2]) <= 20 else "19"  # We will assume its a newer season until 2020/21, from there we complete 1921/22
        return f"{prefix}{season.replace('-', '/')}"  # Handle both possible formats here
    elif len(season) == 4:  # One full year --> 1996
        return f"{str(int(season) - 1)}/{season[-2:]}"  # Take the full year before the given season + Last two digits of original season
    elif len(season) == 2:  # Short one year format --> 96
        prefix = "20" if int(season) <= 20 else "19"  # We will assume its a newer season until 2020/21, from there we complete 1921/22
        full_year = f"{prefix}{season}"
        return f"{str(int(full_year) - 1)}/{season[-2:]}"  # Take the full year before the given season + Last two digits of original season
    else:
        return season


def extract_season_details_from_maccabipedia_as_html_text(season):
    """
    Finds the details for the given season, Does not validate the season.
    :param season: Season id, like "1995/96"
    :type season: str
    :rtype: str
    """
    full_season_id = season
    season_url = f"http://{_MACCABIPEDIA_LINK}/עונת_{full_season_id}"
    response = requests.get(season_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        achievements_text_wrapper = soup.find(class_='text sAchievements')
        [br.replace_with("\n") for br in soup.find_all('br')]
        # Fix spaces at the start and end of lines
        formatted_seasons_details = "\n".join([line.strip() for line in achievements_text_wrapper.text.split("\n")])
        return f"פרטים עבור עונת {full_season_id}:" \
               f"\n{formatted_seasons_details}"
    elif response.status_code == 404:
        return f"עונת {season} לא נמצאה, אנא נסה שנית"
    else:
        logger.warning(f"Got {response.status_code} status_code from HTTP GET of: {season_url}")
        return f"התרחשה תקלה במהלך הוצאת הנתונים הרלוונטים על העונה שביקשת, אנא נסה שנית."


def get_profile(profile_name):
    """
    scrapes the given profile from it's page at maccabipedia, parsing the HTML to string and return the info & stats
    :type profile_name: str
    :param profile_name: The name of the given player/staff
    :return: Information and stats of the player/staff people & link to the profile page
    """
    url = _MACCABIPEDIA_LINK + '/' + profile_name
    response = requests.get('http://' + requests.utils.quote(url))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for br in soup.find_all('br'):
            br.replace_with("\n")

        profile = "\n- פרטים אישיים: \n" + soup.find(class_='ppPersonalDetails').text
        profile += "\n- פרטים מקצועיים: \n" + soup.find(class_='ppProDetails').text
        profile += "\n- סטטיסטיקה: \n"
        profile += "\n--- כל המסגרות ---" + soup.find(id='tab1-content').text
        profile += "--- ליגה ---" + soup.find(id='tab2-content').text
        profile += "--- גביע ---" + soup.find(id='tab3-content').text
        profile += "--- אירופה ---" + soup.find(id='tab4-content').text

        "Removing whitespace"
        profile = profile.replace(" גובה:", "גובה:")

        # The href="..." must have double quotation because we have some players with single quotation in their name
        return f'<a href="{url}" >פרופיל {profile_name.replace("_", " ")}:</a>\n{profile} \n\n'
    elif response.status_code == 404:
        return "לא נמצא שחקן בשם זה. נסו שוב"
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
    telegram_html_text = "\n".join(f'<a href="{_MACCABIPEDIA_LINK}/{player_name}">{player_name}</a>: {amount}'
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
    telegram_html_text = "\n".join(f'<a href="{_MACCABIPEDIA_LINK}/{player_name}">{player_name}</a>: {maccabi_games.hebrew_representation}'
                                   for player_name, maccabi_games in top_players_with_maccabi_games)
    return telegram_html_text


def transform_teams_with_maccabi_games_to_telegram_html_text(top_teams_with_maccabi_games):
    """
    Transforms the given list of teams with maccabi games (probably list of teams streaks, like winning streak)
    into html text that will be sent to the user (including links for the teams).
    :param top_teams_with_maccabi_games: The teams with the maccabi games
    :type top_teams_with_maccabi_games: list of (str, maccabistats.stats.maccabi_games_stats.MaccabiGamesStats)
    :return: The top teams as html text (With maccabipedia links to the teams)
    :rtype: str
    """

    def remove_double_quotation(team_name):
        return team_name.replace('"', '')

    # The href="..." must have double quotation because we have some teams with single quotation in their name
    # We remove the double quotation just be sure they wont be unescaped here
    telegram_html_text = "\n".join(
        f'<a href="{_MACCABIPEDIA_LINK}/{remove_double_quotation(team_name)}">{team_name}</a>: {maccabi_games.hebrew_representation}'
        for team_name, maccabi_games in top_teams_with_maccabi_games)
    return telegram_html_text
