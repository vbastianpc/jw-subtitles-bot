from os import listdir, path
from pathlib import Path
from typing import Any, Dict, List, Union

from yaml import safe_load

# https://github.com/TeamUltroid/Ultroid/tree/main/strings
# http://www.loc.gov/standards/iso639-2/php/English_list.php
languages = {}

STRING_PATH = Path('./strings')

for file in STRING_PATH.glob('*.yml'):
    code = file.stem
    languages[code] = safe_load(open(file, encoding="UTF-8")),


def get_string(lang: str, key: str) -> Any:
    try:
        return languages[lang][key]
    except KeyError:
        return languages["en"][key]        


def get_languages() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }