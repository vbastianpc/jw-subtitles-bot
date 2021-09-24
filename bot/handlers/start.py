from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode
from telegram.ext import CommandHandler

from bot.utils.decorators import log
from bot.utils import SAMPLE_URL, SECCION_DE_VIDEOS

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

start_handler = CommandHandler('start', start)
