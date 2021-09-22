from pathlib import Path
import logging
from functools import wraps
import requests
import os
from io import StringIO

from telegram import Update
from telegram import ParseMode
from telegram import InputMediaDocument
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import Updater

import api_subtitles as subs


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


SAMPLE_URL = 'https://www.jw.org/en/library/videos/#es/mediaitems/VODBibleCreation/docid-502200113_1_VIDEO'
SAMPLE2_URL = 'https://www.jw.org/finder?srcid=share&wtlocale=S&lank=docid-502200113_1_VIDEO'
SECCION_DE_VIDEOS = '[sección de videos](https://www.jw.org/es/biblioteca/videos)'


def log(func):
    @wraps(func)
    def log_function(update: Update, context: CallbackContext, **kwargs):
        user = update.effective_user
        logger.info('%s %s %s', user.id, user.full_name, update.message.text)
        return func(update, context, **kwargs)
    return log_function


@log
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f'Hola {update.effective_user.first_name}.\n\nBusca un video en la app JW Library o en la {SECCION_DE_VIDEOS} '
        'en el idioma que quieras. Comparte conmigo el enlace y te mandaré los subtítulos.\n\n'
        f'Copia [este enlace]({SAMPLE_URL}) como ejemplo y envíamelo.\n\n'
        'Pulsa /help para aprender cómo usar el archivo de subtítulos.',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@log
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Cuando me mandes un enlace de video de JW.ORG te enviaré dos archivos:\n\n'
        '- Archivo `.txt` para leer la transcripción.\n'
        '- Archivo `.vtt` de subtítulos para abrir en un reproductor de videos.',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    if context.bot_data.get('message_id'):
        context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=context.bot_data.get('from_chat_id'),
            message_id=context.bot_data.get('message_id'),
        )
    else:
        msg = context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=open('./how_to_vtt.mp4', 'rb'),
            caption='Puedes usar el reproductor [VLC](https://www.videolan.org/vlc/) para ver el video con subtítulos.',
            parse_mode=ParseMode.MARKDOWN,
        )
        context.bot_data['message_id'] = msg.message_id
        context.bot_data['from_chat_id'] = msg.chat_id


@log
def send_subtitle(update: Update, context: CallbackContext):
    jwurl = update.message.text
    try:
        code_lang, lank = subs.parse_jwurl(jwurl)
        data = subs.get_datajson(code_lang, lank)
        url_subtitle = subs.get_url_subtitles(data)
    except (subs.LankNotFound, ValueError, IndexError):
        text = f'En esta página no hay contenido multimedia para extraer subtítulos. Busca en la {SECCION_DE_VIDEOS} o en la app JW Library y mándame el enlace del video'
    except subs.CodeLangNotFound as e:
        text = f'{e.code_lang!r} no es un idioma válido'
    except subs.SubtitleNotFound as e:
        text = f'Lo siento, no existen subtítulos para el video\n*{e.title}*'
    else:
        title = subs.get_title(data)
        logger.info('%s %s', title, url_subtitle)
        text_subtitles = requests.get(url_subtitle).content.decode()
        text_transcription = title + '\n\n\n' + subs.parse_vtt(text_subtitles)
        try:
            update.message.reply_photo(subs.get_image(data))
        except:
            pass
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaDocument(StringIO(text_transcription), filename=Path(url_subtitle).stem + '.txt'),
                InputMediaDocument(StringIO(text_subtitles), filename=Path(url_subtitle).name,
                                   caption=f'[{title}]({jwurl})', parse_mode=ParseMode.MARKDOWN),
            ],
        )
        return
    logger.info(text)
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def logfile(update: Update, context: CallbackContext):
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open('./log.log', 'rb'),
    )


subtitle_handler = MessageHandler(Filters.regex('https://www.jw.org'), send_subtitle)
logfile_handler = CommandHandler('logfile', logfile)
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)


if __name__ == '__main__':
    updater = Updater(os.getenv('TOKEN_JWSUBS'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(subtitle_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(logfile_handler)
    updater.start_polling()
    updater.idle()
