from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode
from telegram.ext import CommandHandler

from bot.utils.decorators import log


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


help_handler = CommandHandler('help', help)
