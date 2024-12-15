
from textblob import TextBlob

def analyze_positive_words(text):
    """
    分析给定英文文本中的积极词汇频率和比例，并返回整体情感分析结果。
    
    参数:
        text (str): 输入的英文文本。
    
    返回:
        dict: 包含以下内容的字典：
            - positive_words (list): 积极词汇列表。
            - positive_count (int): 积极词汇频率。
            - total_count (int): 总词汇数。
            - positive_ratio (float): 积极词汇比例。
            - overall_polarity (float): 文本整体情感极性。
            - overall_subjectivity (float): 文本整体主观性。
    """
    # 创建 TextBlob 对象
    blob = TextBlob(text)
    
    # 分词
    words = blob.words
    
    # 积极词汇（极性 > 0）
    positive_words = [word for word in words if TextBlob(word).sentiment.polarity > 0]
    
    # 统计积极词汇频率
    positive_count = len(positive_words)
    
    # 总词汇数
    total_count = len(words)
    
    # 计算积极词汇比例
    positive_ratio = positive_count / total_count if total_count > 0 else 0
    
    # 返回结果
    return {
        "positive_words": positive_words,
        "positive_count": positive_count,
        "total_count": total_count,
        "positive_ratio": positive_ratio,
    }
    
def analyze_negative_words(text):
    """
    分析给定英文文本中的消极词汇频率和比例，并返回整体情感分析结果。
    
    参数:
        text (str): 输入的英文文本。
    
    返回:
        dict: 包含以下内容的字典：
            - negative_words (list): 消极词汇列表。
            - negative_count (int): 消极词汇频率。
            - total_count (int): 总词汇数。
            - negative_ratio (float): 消极词汇比例。
            - overall_polarity (float): 文本整体情感极性。
            - overall_subjectivity (float): 文本整体主观性。
    """
    # 创建 TextBlob 对象
    blob = TextBlob(text)
    
    # 分词
    words = blob.words
    
    # 消极词汇（极性 < 0）
    negative_words = [word for word in words if TextBlob(word).sentiment.polarity < 0]
    
    # 统计消极词汇频率
    negative_count = len(negative_words)
    
    # 总词汇数
    total_count = len(words)
    
    # 计算消极词汇比例
    negative_ratio = negative_count / total_count if total_count > 0 else 0
    
    
    # 返回结果
    return {
        "negative_words": negative_words,
        "negative_count": negative_count,
        "total_count": total_count,
        "negative_ratio": negative_ratio
    }


def get_top_k_words(text, top_k=5):
    """
    提取文本中情感极性最高的前 top_k 积极词汇和情感极性最低的前 top_k 消极词汇。
    
    参数:
        text (str): 输入的英文文本。
        top_k (int): 要提取的积极和消极词汇数量。
    
    返回:
        dict: 包含以下内容的字典：
            - top_positive_words (list): 情感极性最高的 top_k 积极词汇及其极性。
            - top_negative_words (list): 情感极性最低的 top_k 消极词汇及其极性。
    """
    # 创建 TextBlob 对象
    blob = TextBlob(text)
    
    # 分词并计算每个词的情感极性
    word_sentiments = [(word, TextBlob(word).sentiment.polarity) for word in blob.words]
    
    # 按情感极性排序
    word_sentiments_sorted = sorted(word_sentiments, key=lambda x: x[1], reverse=True)
    
    # 提取前 top_k 积极词汇（极性最高）
    top_positive_words = word_sentiments_sorted[:top_k]
    
    # 提取前 top_k 消极词汇（极性最低）
    top_negative_words = word_sentiments_sorted[-top_k:]
    
    # 返回结果
    return top_positive_words, top_negative_words
