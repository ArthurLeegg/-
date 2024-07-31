#COMET相关部署过程省略

import pandas as pd

# 获取文件路径
file_path = input("请输入Excel文件的路径：")

# 检查文件路径是否有效
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"文件 {file_path} 未找到。请检查路径后重试。")
    exit()

# 提取所需列
source_texts = df["原文"].tolist()
reference_texts = df["参考译文"].tolist()
baidu_texts = df["Baidu翻译译文"].tolist()
youdao_texts = df["Youdao翻译译文"].tolist()
google_texts = df["Google翻译译文"].tolist()

# 将内容保存到文本文件
def save_to_file(texts, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in texts:
            f.write(line + '\n')

save_to_file(source_texts, 'src.zh')
save_to_file(reference_texts, 'reference.hyp.en')
save_to_file(baidu_texts, 'baidu.hyp.en')
save_to_file(youdao_texts, 'youdao.hyp.en')
save_to_file(google_texts, 'google.hyp.en')


# 创建数据集
def create_dataset(source_file, translation_file, reference_file):
    with open(source_file, 'r', encoding='utf-8') as src, \
         open(translation_file, 'r', encoding='utf-8') as mt, \
         open(reference_file, 'r', encoding='utf-8') as ref:
        return [{"src": s.strip(), "mt": m.strip(), "ref": r.strip()} for s, m, r in zip(src, mt, ref)]

data_baidu = create_dataset('src.zh', 'baidu.hyp.en', 'reference.hyp.en')
data_youdao = create_dataset('src.zh', 'youdao.hyp.en', 'reference.hyp.en')
data_google = create_dataset('src.zh', 'google.hyp.en', 'reference.hyp.en')

# 使用模型进行评分
comet_scores_baidu = model.predict(data_baidu, batch_size=8)
comet_scores_youdao = model.predict(data_youdao, batch_size=8)
comet_scores_google = model.predict(data_google, batch_size=8)

# 提取COMET分数
def extract_scores(predictions):
    # 对于每一个 Prediction 对象，提取 `scores` 中的第一个分数
    return predictions[0]

comet_scores_baidu = extract_scores(comet_scores_baidu)
comet_scores_youdao = extract_scores(comet_scores_youdao)
comet_scores_google = extract_scores(comet_scores_google)

# 将COMET分数添加到DataFrame
df["Baidu翻译COMET Score"] = comet_scores_baidu
df["Youdao翻译COMET Score"] = comet_scores_youdao
df["Google翻译COMET Score"] = comet_scores_google

# 保存结果
df.to_excel(file_path, index=False)
print(f"结果已保存到 {file_path}")