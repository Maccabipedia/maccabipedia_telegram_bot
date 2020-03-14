from maccabipediabot.maccabi_games_filtering import GamesFilter

_USER_DATE_GAMES_FILTER_KEY = "games_filter"


def set_default_filters_for_current_user(update, context):
    context.user_data[_USER_DATE_GAMES_FILTER_KEY] = GamesFilter()