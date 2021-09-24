from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

from bot import create_logger


logger = create_logger(__name__, fmt="%(asctime)s - %(message)s")

def log(func):
    @wraps(func)
    def log_function(update: Update, context: CallbackContext, **kwargs):
        user = update.effective_user
        logger.info('%s %s %s', user.id, user.full_name, update.message.text)
        return func(update, context, **kwargs)
    return log_function

