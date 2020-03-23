import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.parsemode import ParseMode

from maccabipediabot.common import create_maccabipedia_shirt_number_category_html_text, get_song_lyrics, get_profile, \
    get_donation_link_html_text, extract_season_details_from_maccabipedia_as_html_text, format_season_id
from maccabipediabot.handlers_utils import send_typing_action, log_user_request

logger = logging.getLogger(__name__)


def error_callback(update, context):
    """
    Handle all telegram bot related errors
    """
    logger.error("Encountered an error, handling it inside error_callback")
    try:
        raise context.error
    except Unauthorized as e:
        # remove update.message.chat_id from conversation list
        logger.error(e)
    except BadRequest as e:
        # handle malformed requests - read more below!
        logger.error(e)
    except TimedOut as e:
        # handle slow connection problems
        logger.error(e)
    except NetworkError as e:
        # handle other connection problems
        logger.error(e)
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.error(e)
    except TelegramError as e:
        logger.error(e)


@log_user_request
@send_typing_action
def help_handler(update, context):
    """
    Shows the help for this bot.
    """
    user_name = update.effective_chat.username
    if user_name is not None:
        hello_message = f"שלום {user_name}."
    else:
        hello_message = f"שלום."

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"{hello_message}\n"
                                  "בכדי לבחור את קבוצת המשחקים שעליהם תרצה לקבל סטטיסטיקה:"
                                  "\n/create_games_set"
                                  "\n\nבכדי לצפות בסטטיסטיקות כלשהן:"
                                  "\n/games_set"
                                  "\n\nבכדי לצפות בסטטיסטיקה על עונה כלשהי:"
                                  f"\n/season 1995/96"
                                  f"\n\nבכדי לתרום למכביפדיה:"
                                  f"\n/donate"
                                  f"\n\nבכל שלב ניתן לחזור לתפריט העזר באמצעות הפקודה: /help")


@log_user_request
@send_typing_action
def unknown_message_handler(update, context):
    """
    For any msg that we didn't registered explicit
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="הפקודה האחרונה לא הובנה, נסו להשתמש ב: /help")


@log_user_request
@send_typing_action
def start_handler(update, context):
    """
    First msg the user sees
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"שלום {update.effective_chat.username}")

    help_handler(update, context)


@log_user_request
@send_typing_action
def shirt_number_handler(update, context):
    """
    Send link ot the category of player who played with the given shirt number
    """
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"מספר חולצה לא התקבל, בכדי לבדוק למשל אילו שחקנים שיחקו עם חולצה מספר 10, שלח:"
                                      f"\n/shirt_number 10")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=create_maccabipedia_shirt_number_category_html_text(context.args[0]))


@log_user_request
@send_typing_action
def song_handler(update, context):
    """
    :return: Lyrics of the given song & link to the page
    """

    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"שם שיר לא התקבל. בכדי לקבל מילות שיר, למשל, שיר הקונטרה, שלח:"
                                      f"\n/song הקונטרה")
    else:
        song_name = "_".join(context.args[:])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=get_song_lyrics(song_name))


@log_user_request
@send_typing_action
def profile_handler(update, context):
    """
    handle profiles of players. Will be extended to all staff people later
    :return: parsed profile data of the given player
    """

    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"שם שחקן לא התקבל. בכדי לקבל מידע על שחקן, למשל, שרן ייני, שלח:"
                                      f"\n/profile שרן ייני")
    else:
        profile_name = "_".join(context.args[:])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=get_profile(profile_name))


@log_user_request
@send_typing_action
def season_details_handler(update, context):
    """
    Shows the given season details, such as wins/losses/ties amount and which titles maccabi won in this season
    """
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="נא הכנס את העונה אותה תרצה לראות"
                                      "\nלמשל:"
                                      "\n/season 1995/96")
    else:
        full_season_id = format_season_id(context.args[0])
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                 text=extract_season_details_from_maccabipedia_as_html_text(full_season_id))


@log_user_request
@send_typing_action
def donation_handler(update, context):
    """
    Returns the donation page link from maccabipedia
    """

    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                             text=f"אנחנו מזמינים אתכם לתרום למכביפדיה.\n"
                                  f"לצורך המשך הפעילות, בשביל הוספה של תכנים חדשים ויכולות חדשות.\n"
                                  f"בכדי לתרום, היכנסו ל:\n"
                                  f"{get_donation_link_html_text()}")
