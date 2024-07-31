import requests
import uuid
import time
import hashlib
from api_keys import YOUDAO_APP_KEY, YOUDAO_APP_SECRET

YOUDAO_URL = 'https://openapi.youdao.com/api'

def youdao_translate(source_lang, target_lang, text):
    return get_youdao_translation(source_lang, target_lang, text)

def get_youdao_translation(source_lang, target_lang, text):
    data = {
        'from': source_lang,
        'to': target_lang,
        'signType': 'v3',
        'appKey': YOUDAO_APP_KEY,
        'q': text,
        'salt': str(uuid.uuid1()),
        'curtime': str(int(time.time()))
    }
    signStr = YOUDAO_APP_KEY + truncate(data['q']) + data['salt'] + data['curtime'] + YOUDAO_APP_SECRET
    data['sign'] = encrypt(signStr)
    
    response = requests.post(YOUDAO_URL, data=data)
    result = response.json()
    
    if 'translation' in result:
        return {'source': text, 'translation': result['translation'][0]}
    else:
        return {'error': 'Translation failed'}

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()
