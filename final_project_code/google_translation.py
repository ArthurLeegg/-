import requests
import html
from api_keys import GOOGLE_API_KEY

GOOGLE_URL = "https://google-translate1.p.rapidapi.com/language/translate/v2"

def google_translate(source_lang, target_lang, text):
    payload = {
        "q": text,
        "target": target_lang,
        "source": source_lang
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": GOOGLE_API_KEY,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(GOOGLE_URL, data=payload, headers=headers)
    translated_text = response.json()['data']['translations'][0]['translatedText']
    # 解码 Google 翻译结果中的 HTML 实体编码
    translated_text = html.unescape(translated_text)
    return {'source': text, 'translation': translated_text}
