from bot.handlers.start import start_handler
from bot.handlers.help import help_handler
from bot.handlers.subtitle import subtitle_handler
from bot.handlers.logs import logfile_handler, logs_handler, error_handler

handlers = [
    start_handler,
    help_handler,
    subtitle_handler,
    logs_handler,
    logfile_handler
]