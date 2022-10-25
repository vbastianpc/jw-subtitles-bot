from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



x_callback = 'vlc-x-callback://x-callback-url/stream?url=https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'

def test(update: Update, context: CallbackContext):
    update.message.reply_text(f'[x-callback]({x_callback})', parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(f'<a href="{x_callback}">Play on VLC</a>', parse_mode=ParseMode.HTML)
    button = InlineKeyboardButton('Haz click', url=x_callback)
    update.message.reply_text(
        'Play on VLC',
        reply_markup=InlineKeyboardMarkup([[button]])
    )

test_handler = CommandHandler('test', test)