from pathlib import Path
from io import BytesIO
from io import BufferedReader
import logging
import requests
import os

from telegram import Update, parsemode
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import Updater

from api_subtitles import get_subtitles
from api_subtitles import CodeLangNotFound
from api_subtitles import SubtitleNotFound


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


SAMPLE_URL = 'https://www.jw.org/en/library/videos/#es/mediaitems/VODBibleCreation/docid-502200113_1_VIDEO'
SAMPLE2_URL = 'https://www.jw.org/finder?srcid=share&wtlocale=S&lank=docid-502200113_1_VIDEO'
SECCION_DE_VIDEOS = '[Sección de Videos](https://www.jw.org/es/biblioteca/videos)'

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hola. Envíame el link a un video desde la {SECCION_DE_VIDEOS} '
                              'de JW y te entregaré sus subtítulos. Prueba con estos ejemplos:')
    update.message.reply_text(SAMPLE_URL, disable_web_page_preview=True)
    update.message.reply_text(SAMPLE2_URL, disable_web_page_preview=True)
    return


def send_subtitle(update: Update, context: CallbackContext):
    if update.effective_user.id != 58736295:
        context.bot.forward_message(chat_id=58736295, from_chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    try:
        url_subtitle = get_subtitles(update.message.text)
    except ValueError:
        text = f'No parece una url válida\. Elige un video desde la {SECCION_DE_VIDEOS} y mándame el link\n'
    except CodeLangNotFound as e:
        text = f'{e.code_lang!r} no parece un idioma válido'
    except SubtitleNotFound:
        text = 'Parece que este video no tiene subtítulos disponibles'
    else:
        file = BufferedReader(BytesIO(requests.get(url_subtitle).content))
        update.message.reply_document(document=file, filename=Path(url_subtitle).name)
        return
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def log_error(update: Update, context: CallbackContext):
    text = f'{type(context.error)} {context.error}'
    if update.effective_message:
        text += f'\n\n{update.effective_message.text}'
    if update.effective_user:
        text += f'\n\n{update.effective_user.full_name} {update.effective_user.id}'
    context.bot.send_message(chat_id=58736295, text=text)


subtitle_handler = MessageHandler(Filters.regex('https://www.jw.org'), send_subtitle)
start_handler = CommandHandler('start', start)


if __name__ == '__main__':
    updater = Updater(os.getenv('TOKEN_JWSUBS'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(subtitle_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(log_error)
    updater.start_polling()
    updater.idle()
