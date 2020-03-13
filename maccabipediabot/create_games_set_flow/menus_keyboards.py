from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from maccabipediabot.create_games_set_flow.menus_options import GamesFilteringMainMenuOptions, HomeAwayFilteringMenuOptions, TeamFilteringMenuOptions, \
    CompetitionFilteringMenuOptions, DateFilteringMenuOptions


def show_home_away_menu(update, context):
    buttons = [
        [InlineKeyboardButton("משחקי בית", callback_data=HomeAwayFilteringMenuOptions.HOME),
         InlineKeyboardButton("משחקי חוץ", callback_data=HomeAwayFilteringMenuOptions.AWAY),
         InlineKeyboardButton("גם וגם", callback_data=HomeAwayFilteringMenuOptions.ALL_HOME_AWAY)]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="משחקי בית, חוץ או כולם?", reply_markup=reply_markup)


def show_competition_menu(update, context):
    buttons = [
        [InlineKeyboardButton("ליגה", callback_data=CompetitionFilteringMenuOptions.LEAGUE_ONLY),
         InlineKeyboardButton("כל המסגרות", callback_data=CompetitionFilteringMenuOptions.ALL_COMPETITIONS)]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="באיזה מפעל?", reply_markup=reply_markup)


def show_date_menu(update, context):
    buttons = [
        [InlineKeyboardButton("החל מקום המדינה", callback_data=DateFilteringMenuOptions.SINCE_COUNTRY),
         InlineKeyboardButton("כל הזמן", callback_data=DateFilteringMenuOptions.ALL_TIME)]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="באילו תאריכים?", reply_markup=reply_markup)


def show_team_menu(update, context):
    buttons = [
        [InlineKeyboardButton("קבוצה ספציפית", callback_data=TeamFilteringMenuOptions.SPECIFIC_TEAM),
         InlineKeyboardButton("כל הקבוצות", callback_data=TeamFilteringMenuOptions.ALL_TEAMS)]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="נגד איזו קבוצה?", reply_markup=reply_markup)


def show_games_filter_main_menu(update, context):
    buttons = [
        [InlineKeyboardButton("ביתיות", callback_data=GamesFilteringMainMenuOptions.HOME_AWAY),
         InlineKeyboardButton("מפעל", callback_data=GamesFilteringMainMenuOptions.COMPETITION),
         InlineKeyboardButton("יריבה", callback_data=GamesFilteringMainMenuOptions.TEAM),
         InlineKeyboardButton("תאריך", callback_data=GamesFilteringMainMenuOptions.DATE)],

        [InlineKeyboardButton("סיים", callback_data=GamesFilteringMainMenuOptions.FINISH)]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="סנן משחקים לפי:", reply_markup=reply_markup)
