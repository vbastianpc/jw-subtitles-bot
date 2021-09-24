from telegram.ext import Updater
from telegram.constants import MAX_MESSAGE_LENGTH

from bot import create_logger, TOKEN
from bot.handlers import handlers, error_handler


logger = create_logger(__name__)
logger.info('Iniciando bot')


updater = Updater(TOKEN)
updater.start_polling()
for handler in handlers:
    updater.dispatcher.add_handler(handler)
updater.dispatcher.add_error_handler(error_handler)
updater.idle()
