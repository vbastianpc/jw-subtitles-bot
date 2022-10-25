from uuid import uuid4

from telegram import InlineQueryResultArticle

from telegram import ParseMode
from telegram import InputTextMessageContent
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import InlineQueryHandler

import api_subtitles as subs


def inline_languages(update: Update, context: CallbackContext):
    lank = update.inline_query.query
    data = subs.get_datajson('S', lank)
    lang_codes = subs.get_availables_langs(data)

    zip_gen = zip(
        lang_codes,
        map(subs.get_language_name, lang_codes),
        [subs.get_title(data)] * len(lang_codes)
    )
    results = [InlineQueryResultArticle(
        id=str(uuid4()),
        title=f'{lang_code} - {lang_name}',
        input_message_content=InputTextMessageContent(message_text=subs.generate_jwurl(lang_code, lank)),
        description=title,
    ) for lang_code, lang_name, title in zip_gen]
    update.inline_query.answer(results, auto_pagination=True)


inline_handler = InlineQueryHandler(inline_languages)