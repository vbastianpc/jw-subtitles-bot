import json
from pathlib import Path
import requests


LANG_PATH = Path('languages.json')

def write_langs():
    json.dump(
        requests.get('https://data.jw-api.org/mediator/v1/languages/S/all').json()['languages'],
        LANG_PATH.open('w', encoding='utf-8'),
        ensure_ascii=False,
        indent=2,
    )
write_langs()

LANGUAGES = json.load(LANG_PATH.open(encoding='utf-8'))
API_MEDIATOR = 'https://b.jw-cdn.org/apis/mediator/v1/media-items/{code_lang}/{lank}?clientType=www'
API_MEDIATOR_CAT = 'https://b.jw-cdn.org/apis/mediator/v1/categories/{code_lang}/{category}?detailed=1&clientType=www'
API_PUBMEDIA = 'https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS?docid={docid}&output=json&fileformat=mp4,3gp,mp3&alllangs=1&track=1&langwritten={code_lang}&txtCMSLang={code_lang}'
_GET_CATEGORY = 'https://www.jw.org/es/biblioteca/videos/?item=pub-jwb-082_1_VIDEO&appLanguage=S'
SEARCH = 'https://data.jw-api.org/search/query'
SAMPLE_URL = 'https://www.jw.org/finder?srcid=jwlshare&wtlocale=S&lank=pub-jwb-082_1_VIDEO'
SAMPLE_URL2 = 'https://www.jw.org/es/biblioteca/videos/#es/mediaitems/StudioMonthlyPrograms/pub-jwb-082_1_VIDEO'
SECCION_DE_VIDEOS = '[sección de videos](https://www.jw.org/es/biblioteca/videos)'
