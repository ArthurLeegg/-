from zhipuai import ZhipuAI
from api_keys import ZHIPU_API_KEY
from api_keys import system_message


def get_mqm_score(source_text, translated_text):
    client = ZhipuAI(api_key=ZHIPU_API_KEY)

    input_text = f"英文：{source_text};中文：{translated_text}"
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text},
        ],
        stream=True,
    )

    content = ""
    for chunk in response:
        content += chunk.choices[0].delta.content
    return content
