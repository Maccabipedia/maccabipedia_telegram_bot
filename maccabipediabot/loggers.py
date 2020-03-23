import logging
from pathlib import Path

maccabipedia_bot_root_folder_path = Path.home()
maccabipedia_bot_log_path = maccabipedia_bot_root_folder_path / "maccabipedia_bot_logs" / "all_logs.txt"


def initialize_loggers():
    # Ensure logging folder exists
    maccabipedia_bot_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Root logger, so all other logger will inherit those handlers.
    logger = logging.getLogger("maccabipediabot")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s --- %(funcName)s(l.%(lineno)d) :: %(message)s')

    debug_handler = logging.FileHandler(str(maccabipedia_bot_log_path), 'w', encoding="utf-8")
    debug_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    logger.addHandler(debug_handler)
    logger.addHandler(stdout_handler)

    logger.debug("Initialize loggers (File and Stdout)")
