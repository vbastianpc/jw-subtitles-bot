import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
import random
from io import StringIO
import re

import webvtt


from bot.utils import API_DOCID, API_PUB, LANGUAGES, API_MEDIATOR
from bot import create_logger


logger = create_logger(__name__)


class SubtitleNotFound(Exception):
    def __init__(self, title, lang_name):
        self.title = title
        self.lang_name = lang_name

class PubMediaNotFound(Exception):
    pass

class Publication:
    def __init__(self):
        self.docid = None
        self.lang_code = None
        self.lank = None
        self.pub = None
        self.track = None
    
    def url_api(self):
        return

    def url_vtt(self):
        return
    
    def url_video(self):
        return

class JWURLParser:
    def __init__(self, jwurl):
        self.jwurl = jwurl
    
    def scrappy(self):
        response = requests.get(self.jwurl, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
        pattern = r'data-jsonurl=["\'](https:[\w\-\./]+GETPUBMEDIALINKS\?[\w=&%]+)["\']'
        match = re.search(pattern, response.content.decode())
        return match.group(1)

# browser.page.find('body').get('class') buscar pub y generar link pubmedialink

# class JWSubtitles
# class JWSubtitlesLank
# class JWSubtitlesDocid
class Subtitles:
    def __init__(self, jwurl=None, lang_code=None, lank=None, docid=None, pub=None, track=None):
        if jwurl:
            lang_code, lank, docid, pub, track = self.parse_jwurl()
        if lang_code:
            if lank:
                url_api = API_MEDIATOR.format(lang_code=lang_code, lank=lank)
            elif docid:
                url_api = API_DOCID.format(lang_code=lang_code, docid=docid)
            elif pub and track:
                url_api = API_PUB.format(lang_code=lang_code, pub=pub, track=track)
            else:
                raise TypeError("some required argument missing 'lank', 'docid' or ('pub' and 'track')")
        else:
            raise TypeError("missing required argument 'lang_code'")
        print(url_api)
        return
        data = requests.get(url_api).json()


        self.url_subtitles = self.get_url_subtitles()
        self.text_subtitles = self.get_text_subtitles(self.url_subtitles)
        self.text_transcription = self.get_text_transcription(self.text_subtitles, self.title)
        self.photo = None

    def parse_jwurl(self):
        up = urlparse(self.url)
        pq = parse_qs(up.query)
        lang_code = lank = docid = pub = track = None
        if up.path == '/finder':
            lang_code = pq['wtlocale'][0]
            lank = pq.get('lank', [''])[0]
            docid = pq.get('docid', [''])[0]
        elif '/mediaitems/' in up.fragment:
            locale, _, _, self.lank = up.fragment.split('/')
            lang_code = self.get_lang_code(self.locale)
        elif 'jw.org' in up.netloc:
            self.locale = up.path.split('/')[1]
            self.lang_code = self.get_lang_code(self.locale)
        else:
            raise ValueError(f'{self.url!r} no es un enlace válido')
        return lang_code, lank, docid, pub, track

    @staticmethod
    def get_lang_code(locale):
        for language in LANGUAGES:
            if language['locale'] == locale:
                return language['code']
        else:
            raise ValueError(f'No existe el idioma locale={locale}')

    def get_language_name(self):
        for language in LANGUAGES:
            if language['code'] == self.lang_code:
                return language['name']
        else:
            raise ValueError(f'No existe el idioma code={self.lang_code}')
    
    def get_language_vernacular(self):
        for language in LANGUAGES:
            if language['code'] == self.lang_code:
                return language['vernacular'].capitalize()
        else:
            raise ValueError(f'No existe el idioma code={self.lang_code}')

    def generate_jwurl(self):
        base = f'https://www.jw.org/finder?srcid=share&wtlocale={self.lang_code}'
        return base + f'&lank={self.lank}' if self.lank else f'&docid={self.docid}'

    def _subs_from_json(self):
        if self.lank:
            url = API_MEDIATOR.format(lang_code=self.lang_code, lank=self.lank)
            data = requests.get(url).json()
        elif self.docid:
            url = API_PUBMEDIA.format(lang_code=self.lang_code, docid=self.docid)
            data = requests.get(url).json()
        else:
            raise PubMediaNotFound
        if not data['media']:
            raise PubMediaNotFound
        logger.info('[%s %s %s](%s)', self.lang_code, self.lank, self.docid, url)
        self.title = data['media'][0]['title']
        for file in data['media'][0]['files']:
            if file.get('subtitles'):
                break
        else:
            raise SubtitleNotFound
        return file['subtitles']['url']

    def _subs_from_scrappy(self):
        browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
        response = browser.open(self.url)
        response = browser.page.find

    def get_url_subtitles(self):
        try:
            return self._subs_from_json()
        except PubMediaNotFound:
            pass

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
