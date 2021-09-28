from telegram.ext import Updater
from bot import create_logger, TOKEN
from bot.handlers import handlers
from bot.handlers.logs import error_handler


logger = create_logger(__name__)
logger.info('Iniciando bot')

updater = Updater(TOKEN)
for handler in handlers:
    updater.dispatcher.add_handler(handler)
updater.dispatcher.add_error_handler(error_handler)
updater.start_polling()
updater.idle()
