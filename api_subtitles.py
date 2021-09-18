import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from io import StringIO

import webvtt


API_MEDIATOR = 'https://b.jw-cdn.org/apis/mediator/v1/media-items/{code_lang}/{lank}?clientType=www'
API_MEDIATOR_CAT = 'https://b.jw-cdn.org/apis/mediator/v1/categories/{code_lang}/{category}?detailed=1&clientType=www'
API_PUBMEDIA = 'https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS?docid={docid}&output=json&fileformat=mp4,3gp,mp3&alllangs=1&track=1&langwritten={code_lang}&txtCMSLang={code_lang}'


class CodeLangNotFound(Exception):
    def __init__(self, code_lang):
        self.code_lang = code_lang


class SubtitleNotFound(Exception):
    pass


def get_code_lang(locale):
    url = 'https://data.jw-api.org/mediator/v1/languages/S/all'
    list_langs = requests.get(url).json()['languages']
    for lang in list_langs:
        if lang['locale'] == locale:
            return lang['code']
    else:
        raise CodeLangNotFound(locale)


def get_subtitles_from_mediator(code_lang, lank):
    url = API_MEDIATOR.format(code_lang=code_lang, lank=lank)
    data = requests.get(url).json()
    print(url)
    for file in data['media'][0]['files']:
        if file.get('subtitles'):
            break
    else:
        raise SubtitleNotFound
    return file['subtitles']['url']


def get_url_subtitles(url):
    up = urlparse(url)
    pq = parse_qs(up.query)
    if up.path == '/finder':
        code_lang, lank = pq['wtlocale'][0], pq['lank'][0]
    elif '/mediaitems/' in up.fragment:
        locale, _, category, lank = up.fragment.split('/')
        code_lang = get_code_lang(locale)
    else:
        raise ValueError(f'{url!r} it is not a valid url')
    return get_subtitles_from_mediator(code_lang, lank)


def parse_vtt(text_vtt):
    text = ''
    for caption in webvtt.read_buffer(StringIO(text_vtt)):
        print(f'{caption.text!r}')
        text += caption.text.replace('\n', ' ') + '\n'
        if caption.text.strip().endswith('.'):
            text += '\n'
    return text


if __name__ == '__main__':
    urls = [
        'https://www.jw.org/finder?srcid=share&wtlocale=S&lank=docid-502200113_1_VIDEO',
        'https://www.jw.org/en/library/videos/#es/mediaitems/VODBibleCreation/docid-502200113_1_VIDEO',
        'https://www.jw.org/es/biblioteca/videos/#es/mediaitems/StudioMonthlyPrograms/pub-jwb-082_1_VIDEO',
        'https://www.jw.org/finder?srcid=share&wtlocale=S&lank=pub-jwb-082_1_VIDEO'
    ]
    for url in urls:
        print(get_url_subtitles(url))
    print('FIN')