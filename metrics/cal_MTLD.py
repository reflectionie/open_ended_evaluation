import re
from nltk.corpus import stopwords
from lexical_diversity import lex_div as ld

def calculate_mtld(text, remove_stopwords=False):
    """
    计算给定文本的 MTLD（Measure of Textual Lexical Diversity）得分。

    参数：
    - text (str): 输入的文本
    - remove_stopwords (bool): 是否移除停用词（默认为 False）

    返回：
    - float: 计算得到的 MTLD 分数
    """
    # 1. 转为小写
    text_lower = text.lower()

    # 2. 去除标点符号（只保留字母和数字）
    text_clean = re.sub(r'[^\w\s]', '', text_lower)

    # 3. 拆分为单词
    words = text_clean.split()

    # 4. 可选：去除停用词
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

    # 5. 计算 MTLD
    mtld_score = ld.mtld(words)
    return mtld_score

# 测试示例
if __name__ == "__main__":
    sample_text = "The cat chased the mouse. The Mouse ran away. The CAT chased again."
    mtld_score = calculate_mtld(sample_text, remove_stopwords=True)  # 可选择是否去除停用词
    print(f"MTLD Score: {mtld_score}")
