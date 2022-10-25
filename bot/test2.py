from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater


my_x_callback = 'vlc-x-callback://x-callback-url/stream?url=https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'

def test(update: Update, context: CallbackContext):
    url_video = context.args[0]
    netlify = f'https://laughing-borg-85bce4.netlify.app?url={url_video}'
    button = InlineKeyboardButton('Play it on VLC', url=netlify)
    update.message.reply_text(
        'Testing InlineKeyboard',
        reply_markup=InlineKeyboardMarkup([[button]])
    )

if __name__ == '__main__':
    updater = Updater('795399285:AAHPMGzEuRG-tKfVD9PnxrSeg-S8I5O9Pjo')
    updater.dispatcher.add_handler(CommandHandler('test', test))
    updater.start_polling()
    updater.idle()
