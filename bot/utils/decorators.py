from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_markdown, escape_markdown

from bot import create_logger


logger = create_logger(__name__, fmt="%(asctime)s - %(message)s")

def log(func):
    @wraps(func)
    def log_function(update: Update, context: CallbackContext, **kwargs):
        user = update.effective_user
        logger.info('%s %s', mention_markdown(user.id, user.first_name), escape_markdown(update.message.text))
        return func(update, context, **kwargs)
    return log_function

