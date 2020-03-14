from maccabipediabot.maccabi_games_filtering import GamesFilter

_USER_DATE_GAMES_FILTER_KEY = "games_filter"
_MACCABIPEDIA_LINK = "www.maccabipedia.co.il"


def set_default_filters_for_current_user(update, context):
    context.user_data[_USER_DATE_GAMES_FILTER_KEY] = GamesFilter()


def create_maccabipedia_shirt_number_category_html_text(shirt_number):
    return f"<a href='{_MACCABIPEDIA_LINK}/קטגוריה:שחקנים_שלבשו_מספר_{shirt_number}'>שחקנים שלבשו מספר {shirt_number}</a>"


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
