import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
import random
from io import StringIO

import webvtt

from bot.utils import LANGUAGES, API_MEDIATOR
from bot import create_logger


logger = create_logger(__name__)


class SubtitleNotFound(Exception):
    def __init__(self, title, lang_name):
        self.title = title
        self.lang_name = lang_name

class PubMediaNotFound(Exception):
    pass


class Subtitles:
    def __init__(self, url, code_lang=None, lank=None):
        self.url = url
        self.code_lang = code_lang
        self.lank = lank
        if not (code_lang and lank):
            self.code_lang, self.lank = self.parse_jwurl()
        self.data = self.get_datajson()
        self.url_subtitles = self.get_url_subtitles()
        self.text_subtitles = self.get_text_subtitles(self.url_subtitles)
        self.text_transcription = self.get_text_transcription(self.text_subtitles, self.get_title())


    def parse_jwurl(self):
        up = urlparse(self.url)
        pq = parse_qs(up.query)
        if up.path == '/finder':
            code_lang = pq['wtlocale'][0]
            lank = pq['lank'][0]
        elif '/mediaitems/' in up.fragment:
            locale, _, _, lank = up.fragment.split('/')
            code_lang = self.get_code_lang(locale)
        else:
            raise ValueError(f'{self.url!r} no es un enlace válido')
        return code_lang, lank

    @staticmethod
    def get_code_lang(locale):
        for language in LANGUAGES:
            if language['locale'] == locale:
                return language['code']
        else:
            raise ValueError(f'No existe el idioma locale={locale}')

    def get_language_name(self):
        for language in LANGUAGES:
            if language['code'] == self.code_lang:
                return language['name']
        else:
            raise ValueError(f'No existe el idioma code={self.code_lang}')
    
    def get_language_vernacular(self):
        for language in LANGUAGES:
            if language['code'] == self.code_lang:
                return language['vernacular'].capitalize()
        else:
            raise ValueError(f'No existe el idioma code={self.code_lang}')

    def generate_jwurl(self):
        return f'https://www.jw.org/finder?srcid=share&wtlocale={self.code_lang}&lank={self.lank}'

    def get_datajson(self):
        url = API_MEDIATOR.format(code_lang=self.code_lang, lank=self.lank)
        logger.info('[%s %s](%s)', self.code_lang, self.lank, url)
        data = requests.get(url).json()
        if not data['media']:
            raise PubMediaNotFound(url)
        return data

    def get_url_subtitles(self):
        for file in self.data['media'][0]['files']:
            if file.get('subtitles'):
                break
        else:
            raise SubtitleNotFound(self.get_title(), self.get_language_name())
        return file['subtitles']['url']

    def get_title(self):
        return self.data['media'][0]['title']

    def get_any_image(self):
        images = []
        for v in self.data['media'][0]['images'].values():
            [images.append(url) for url in v.values()]
        return random.choice(images)
        
    def get_image(self):
        try:
            return self.data['media'][0]['images']['pnr']['lg']
        except KeyError:
            return self.get_any_image()

    def get_availables_langs(self):
        return self.data['media'][0]['availableLanguages']
    
    @staticmethod
    def get_text_subtitles(url_subs):
        return requests.get(url_subs).content.decode()

    @staticmethod
    def get_text_transcription(subtitles='', title=''):
        transcription = title + '\n\n\n' if title else ''
        for caption in webvtt.read_buffer(StringIO(subtitles)):
            transcription += caption.text.replace('\n', ' ') + '\n'
            if caption.text.strip().endswith('.'):
                transcription += '\n'
        return transcription
