import pandas as pd
import json
import re

# 读取 Excel 文件
file_path = 'mqm.xlsx'
df = pd.read_excel(file_path)

# 初始化错误统计字典
error_stats = {
    "Baidu": {},
    "Youdao": {},
    "Google": {}
}

def extract_valid_json(text):
    # 使用正则表达式提取有效的 JSON 部分
    json_match = re.search(r'\{.*\}', str(text), re.DOTALL)
    if json_match:
        return json_match.group(0)
    return None

# 处理每一列中的 JSON 数据
for engine in ["Baidu", "Youdao", "Google"]:
    column_name = f"{engine}翻译MQM Analysis"
    for index, row in df.iterrows():
        cell_data = row[column_name]
        valid_json = extract_valid_json(cell_data)
        if valid_json:
            try:
                json_data = json.loads(valid_json)
                errors = json_data.get("errors", [])
                for error in errors:
                    category = error["category"]
                    count = error.get("count", 0)  # 默认 count 为 0
                    if category in error_stats[engine]:
                        error_stats[engine][category] += count
                    else:
                        error_stats[engine][category] = count
            except (json.JSONDecodeError, KeyError) as e:
                print(valid_json)
                print(f"Error parsing JSON at row {index + 1} in {engine} column: {e}")
        else:
            print(valid_json)
            print(f"No valid JSON found at row {index + 1} in {engine} column")

# 生成统计表格
summary_data = []
for engine, stats in error_stats.items():
    for category, count in stats.items():
        summary_data.append([engine, category, count])

summary_df = pd.DataFrame(summary_data, columns=["Engine", "Error Type", "Total Count"])

# 保存到新的 Excel 文件
output_path = 'error_summary.xlsx'
summary_df.to_excel(output_path, index=False)
output_path
