import os
from tkinter import Tk, ttk, Button
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
from baidu_translation import baidu_translate
from youdao_translation import youdao_translate
from google_translation import google_translate
from glm4_evaluation import get_mqm_score
from bleu_score import calculate_bleu

LANGUAGES = {
    "中文": "zh",
    "英文": "en",
    "法文": "fr",
    "韩文": "ko",
    "日文": "ja"
}

def main():
    root = tk.Tk()
    root.title("语言选择和文件上传")

    source_language_label = ttk.Label(root, text="选择源语言:")
    source_language_label.grid(row=0, column=0, padx=5, pady=5)
    source_language = ttk.Combobox(root, values=list(LANGUAGES.keys()))
    source_language.set("中文")
    source_language.grid(row=0, column=1, padx=5, pady=5)

    target_language_label = ttk.Label(root, text="选择目标语言:")
    target_language_label.grid(row=1, column=0, padx=5, pady=5)
    target_language = ttk.Combobox(root, values=list(LANGUAGES.keys()))
    target_language.set("英文")
    target_language.grid(row=1, column=1, padx=5, pady=5)

    def select_file():
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            translate_and_show(file_path)

    def translate_and_show(file_path):
        translations = {}
        source_lang = LANGUAGES[source_language.get()]
        target_lang = LANGUAGES[target_language.get()]

        # Read input Excel file
        df = pd.read_excel(file_path)
        if "原文" not in df.columns:
            print("Excel文件中必须包含‘原文’列")
            return
        if "参考译文" not in df.columns:
            df["参考译文"] = ""

        data = {
            "原文": [],
            "参考译文": [],
            "Baidu翻译译文": [],
            "Baidu翻译BLEU Score": [],
            "Baidu翻译COMET Score": [],
            "Baidu翻译MQM Analysis": [],
            "Youdao翻译译文": [],
            "Youdao翻译BLEU Score": [],
            "Youdao翻译COMET Score": [],
            "Youdao翻译MQM Analysis": [],
            "Google翻译译文": [],
            "Google翻译BLEU Score": [],
            "Google翻译COMET Score": [],
            "Google翻译MQM Analysis": []
        }

        for index, row in df.iterrows():
            text = row['原文']
            reference_translation = row['参考译文']

            # Baidu Translation
            baidu_translation = baidu_translate(source_lang, target_lang, text)
            translations['baidu'] = baidu_translation

            # Youdao Translation
            youdao_translation = youdao_translate(source_lang, target_lang, text)
            translations['youdao'] = youdao_translation

            # Google Translation
            google_translation = google_translate(source_lang, target_lang, text)
            translations['google'] = google_translation

            for provider, translation in translations.items():
                source_text = translation['source']
                translated_text = translation['translation']

                # Calculate BLEU score if reference translation is provided
                if pd.notna(reference_translation) and reference_translation.strip():
                    bleu_score = calculate_bleu(reference_translation, translated_text)
                else:
                    bleu_score = 0

                mqm_score = get_mqm_score(source_text, translated_text)

                data[f"{provider.capitalize()}翻译译文"].append(translated_text)
                data[f"{provider.capitalize()}翻译BLEU Score"].append(bleu_score)
                data[f"{provider.capitalize()}翻译COMET Score"].append("N/A")  # Placeholder for COMET Score
                data[f"{provider.capitalize()}翻译MQM Analysis"].append(mqm_score)

            data["原文"].append(text)
            data["参考译文"].append(reference_translation)

        # Convert to DataFrame
        result_df = pd.DataFrame(data)

        # Ask user for save location
        save_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if save_path:
            result_df.to_excel(save_path, index=False)
            print(f"Excel file saved to {save_path}")

        root.destroy()

    upload_button = Button(root, text="上传Excel文件", command=select_file)
    upload_button.grid(row=2, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
