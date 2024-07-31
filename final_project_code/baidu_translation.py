import requests
import json
from api_keys import BAIDU_API_KEY, BAIDU_SECRET_KEY

def baidu_translate(source_lang, target_lang, text):
    access_token = get_baidu_access_token()
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + access_token
    payload = json.dumps({
        "from": source_lang,
        "to": target_lang,
        "q": text
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return {'source': result['result']['trans_result'][0]['src'],
            'translation': result['result']['trans_result'][0]['dst']}

def get_baidu_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": BAIDU_API_KEY, "client_secret": BAIDU_SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
