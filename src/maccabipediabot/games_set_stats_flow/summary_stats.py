from common import _USER_DATE_GAMES_FILTER_KEY, transform_stats_to_pretty_hebrew_text
from games_set_stats_flow.common_menu import go_to_more_stats_or_finish_menu
from handlers_utils import log_user_request, send_typing_action
from maccabi_games_filtering import MaccabiGamesFiltering


@log_user_request
@send_typing_action
def show_summary_stats_action(update, context):
    games = MaccabiGamesFiltering(context.user_data[_USER_DATE_GAMES_FILTER_KEY]).filter_games()
    summary_stats = transform_stats_to_pretty_hebrew_text(games.results.json_dict())

    query = update.callback_query
    query.edit_message_text(text=summary_stats)

    return go_to_more_stats_or_finish_menu(update, context)
