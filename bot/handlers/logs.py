import html
import traceback
import json

from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.constants import MAX_MESSAGE_LENGTH
from telegram.ext.filters import Filters

from bot import create_logger, DEV


logger = create_logger(__name__)

def logfile(update: Update, context: CallbackContext):
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open('./log.log', 'rb'),
    )

def logs(update: Update, conttext: CallbackContext):
    with open('./log.log', 'r', encoding='utf-8') as f:
        datalogs = f.read()
    update.message.reply_text(
        text=datalogs[-MAX_MESSAGE_LENGTH::],
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@logs
def fallback_text(update: Update, context: CallbackContext):
    pass

def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
    if DEV:
        context.bot.send_message(chat_id=DEV, text=message, parse_mode=ParseMode.HTML)
    # chunks = [message[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]
    # for chunk in chunks:
    #     context.bot.send_message(chat_id=58736295, text=chunk, parse_mode=ParseMode.HTML)


logfile_handler = CommandHandler('logfile', logfile)
logs_handler = CommandHandler('logs', logs)
fallback_text_handler = MessageHandler(Filters.text, fallback_text)