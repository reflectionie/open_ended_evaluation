import os
import json
def Story_Extraction(base_dir):
    """
    从指定目录中提取所有故事文本。

    参数：
        base_dir (str): 基础目录路径。

    返回：
        list: 包含所有故事文本的列表。
    """
    stories = []
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "story" in data:
                        stories.append(data["story"])
    return stories
