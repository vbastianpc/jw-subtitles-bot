from bot.handlers.start import start_handler
from bot.handlers.help import help_handler
from bot.handlers.subtitle import subtitle_handler
from bot.handlers.logs import logfile_handler, logs_handler, fallback_text_handler
from bot.handlers.test import test_handler

handlers = [
    start_handler,
    help_handler,
    subtitle_handler,
    logs_handler,
    logfile_handler,
    test_handler,
    fallback_text_handler, # always at the end
]