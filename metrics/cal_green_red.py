from metrics.cal_sentiment_score import analyze_sentiment
from metrics.cal_MTLD import calculate_mtld
from metrics.cal_STTR import calculate_normalized_ttr

def evaluate_stories(stories):
    sentiment_polarity_scores = []
    sentiment_subjectivity_scores = []
    mtld_scores = []
    normalized_ttr_scores = []

    for story in stories:
        # 计算情感评分
        polarity, subjectivity = analyze_sentiment(story)
        sentiment_polarity_scores.append(polarity)
        sentiment_subjectivity_scores.append(subjectivity)

        # 计算 MTLD
        mtld_score = calculate_mtld(story)
        mtld_scores.append(mtld_score)

        # 计算归一化 TTR
        normalized_ttr_score = calculate_normalized_ttr(story)
        normalized_ttr_scores.append(normalized_ttr_score)

    # 计算平均值
    avg_sentiment_polarity = sum(sentiment_polarity_scores) / len(sentiment_polarity_scores)
    avg_sentiment_subjectivity = sum(sentiment_subjectivity_scores) / len(sentiment_subjectivity_scores)
    avg_mtld_score = sum(mtld_scores) / len(mtld_scores)
    avg_normalized_ttr = sum(normalized_ttr_scores) / len(normalized_ttr_scores)

    return {
        "average_sentiment_polarity": avg_sentiment_polarity,
        "average_sentiment_subjectivity": avg_sentiment_subjectivity,
        "average_mtld_score": avg_mtld_score,
        "average_normalized_ttr": avg_normalized_ttr,
    }

# 示例用法
# 假设 stories 是生成的故事列表
# stories = ["Story 1 text...", "Story 2 text...", ...]
# result = evaluate_stories(stories)
# print(result)
