from textblob import TextBlob

def analyze_sentiment(text):
    """
    计算输入文本的情感评分。

    参数:
    text (str): 要分析的文本。

    返回:
    tuple: 包含极性和主观性的二元组。
    """
    # 创建 TextBlob 对象
    blob = TextBlob(text)
    
    # 获取情感评分
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    return polarity, subjectivity

# 示例用法
text = "test text"
polarity, subjectivity = analyze_sentiment(text)
# print(f"polarity: {polarity}, subjectivity: {subjectivity}")
