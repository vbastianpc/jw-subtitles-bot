from io import StringIO
from pathlib import Path

from telegram import Update
from telegram import ParseMode
from telegram import InputMediaDocument
from telegram import MessageEntity
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

from bot.utils import SECCION_DE_VIDEOS
from bot.utils.jw import JWURLParser, Subtitles, SubtitleNotFound, PubMediaNotFound
from bot.utils.decorators import log
from bot import create_logger



logger = create_logger(__name__)

@log
def parse_urls(update: Update, context: CallbackContext):
    urls = list(update.message.parse_entities([MessageEntity.URL]).values())
    jwurls = [url for url in urls if url.startswith('https://www.jw.org')]
    print(*jwurls, sep='\n')
    for jwurl in jwurls:
        send_subtitle(update, context, jwurl)
    return


def send_subtitle(update, context, jwurl):
    publication = JWURL(url).parse()
    


    # try:
    #     subs = Subtitles(jwurl)
    # except PubMediaNotFound:
    #     text = f'Lo siento, esta [publicación]({jwurl}) no está disponible'
    # except (ValueError, IndexError, KeyError) as e:
    #     # TODO pedir feedback si está seguro que tiene subtítulos
    #     text = f'No he encontrado subtítulos en [este enlace]({jwurl}). Busca en la {SECCION_DE_VIDEOS} o en la app JW Library y envíame el enlace'
    # except SubtitleNotFound as e:
    #     text = f'Lo siento, no existen subtítulos para el video\n*{e.title}*\nen el idioma *{e.lang_name}*'
    # else:
    #     logger.info('[%s](%s)', subs.get_title(), subs.url_subtitles)
    #     try:
    #         update.message.reply_photo(subs.get_image())
    #     except:
    #         pass
    #     context.bot.send_media_group(
    #         chat_id=update.effective_chat.id,
    #         media=[
    #             InputMediaDocument(
    #                 StringIO(subs.text_transcription),
    #                 filename=Path(subs.url_subtitles).stem + '.txt'
    #             ),
    #             InputMediaDocument(
    #                 StringIO(subs.text_subtitles),
    #                 filename=Path(subs.url_subtitles).name,
    #                 caption=f'[{subs.get_language_vernacular()} - {subs.get_title()}]({subs.generate_jwurl()})',
    #                 parse_mode=ParseMode.MARKDOWN),
    #         ],
    #     )
        return
    logger.info(text)
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


subtitle_handler = MessageHandler(Filters.entity(MessageEntity.URL), parse_urls)
