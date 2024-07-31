from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize

# 函数：计算BLEU分数
def calculate_bleu(reference_translation, translation):
    reference_tokens = word_tokenize(reference_translation)
    translation_tokens = word_tokenize(translation)
    smoothie = SmoothingFunction().method1
    # 计算带平滑函数的BLEU分数
    return sentence_bleu([reference_tokens], translation_tokens, smoothing_function=smoothie)
