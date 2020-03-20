class TopPlayersStatsMenuOptions(object):
    MENU_NAME = "top_players_stats_menu"
    TOP_SCORERS = f"{MENU_NAME}_top_scorers"
    TOP_ASSISTERS = f"{MENU_NAME}_top_assisters"
    MOST_PLAYED = f"{MENU_NAME}_most_played"
    MOST_CAPTAIN = f"{MENU_NAME}_most_captain"

    TEXT = "איזו סטטסטיקה לגבי שחקנים מצטיינים תרצה לראות?"


class PlayersStreaksStatsMenuOptions(object):
    MENU_NAME = "players_streaks_stats_menu"
    WINNING_STREAK = f"{MENU_NAME}_winning_streak"
    UNBEATEN_STREAK = f"{MENU_NAME}_unbeaten_streak"
    SCORE_AT_LEAST_A_GOAL = f"{MENU_NAME}_score_at_least_a_goal"
    CLEAN_SHEETS = f"{MENU_NAME}_clean_sheets"

    TEXT = "בחר את הסטטיסטיקה שעבורה תרצה לראות עבורה את השחקנים בעלי הרצף הארוך ביותר?"


class TeamStreaksStatsMenuOptions(object):
    MENU_NAME = "teams_streaks_stats_menu"
    WINNING_STREAK = f"{MENU_NAME}_winning_streak"
    UNBEATEN_STREAK = f"{MENU_NAME}_unbeaten_streak"
    SCORE_AT_LEAST_A_GOAL = f"{MENU_NAME}_score_at_least_a_goal"
    CLEAN_SHEETS = f"{MENU_NAME}_clean_sheets"

    TEXT = "בחר את הסטטיסטיקה שעבורה תרצה לראות את היריבות בעלי הרצף הארוך ביותר?"


class MoreStatsOrFinishMenuOptions(object):
    MENU_NAME = "more_stats_or_finish_menu"
    MORE_STATS = f"{MENU_NAME}_more_stats"
    FINISH = f"{MENU_NAME}_finish"

    TEXT = "תרצה לצפות בסטטיסטיקה נוספת או לסיים?"


class GamesStatsMainMenuOptions(object):
    MENU_NAME = "games_stats_main_menu"
    TOP_PLAYERS_STATS = f"{MENU_NAME}_top_players"
    PLAYERS_STREAKS_STATS = f"{MENU_NAME}_players_streaks"
    TEAMS_STREAKS_STATS = f"{MENU_NAME}_teams_streaks"
    SUMMARY_STATS = f"{MENU_NAME}_summary"

    FINISH = f"{MENU_NAME}_finish"

    FIRST_TIME_TEXT = "איזו סטטיטיקה תרצה לראות?"
    AFTER_FIRST_TIME_TEXT = "בחר סטטיסטיקה נוספת לצפייה, או סיים:"
