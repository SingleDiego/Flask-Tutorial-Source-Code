import requests
from flask_babel import _

def translate(text, source_language, dest_language):
    """
    type 代码：
    ZH_CN2EN    中文　»　英语
    ZH_CN2JA    中文　»　日语
    ZH_CN2KR    中文　»　韩语
    EN2ZH_CN    英语　»　中文
    JA2ZH_CN    日语　»　中文
    KR2ZH_CN    韩语　»　中文   
    """
    source_language = 'ZH_CN' if source_language.upper()[:2] == 'ZH' else source_language.upper()
    dest_language = 'ZH_CN' if dest_language.upper()[:2] == 'ZH' else dest_language.upper()
    type = '{}2{}'.format(source_language, dest_language)

    url = "http://fanyi.youdao.com/translate?&doctype=json&type={}&i={}".format(type, text)
    r = requests.get(url)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return {'text': r.json()['translateResult'][0][0]['tgt']}