from collections import Counter
from operator import itemgetter

def calculate_dict(female_array, male_array):
    """计算女性和男性的计数字典，确保两者的键空间一致"""
    counter_f_h = Counter(female_array)
    counter_m_h = Counter(male_array)
    for key in set(counter_f_h) - set(counter_m_h):
        counter_m_h[key] = 0
    for key in set(counter_m_h) - set(counter_f_h):
        counter_f_h[key] = 0
    return counter_f_h, counter_m_h

def odds_ratio(f_dict, m_dict, topk=50, threshold=20):
    """计算odds ratio，并返回最高和最低的前topk个词"""
    very_small_value = 0.00001  # 避免除零错误的极小值
    if len(f_dict.keys()) != len(m_dict.keys()):
        raise Exception('The category for analyzing the male and female should be the same!')

    odds_ratio = {}
    total_num_f = sum(f_dict.values())
    total_num_m = sum(m_dict.values())

    for key in f_dict.keys():
        m_num = m_dict[key]
        f_num = f_dict[key]
        non_f_num = total_num_f - f_num
        non_m_num = total_num_m - m_num
        if f_num >= threshold and m_num >= threshold:
            odds_ratio[key] = round((m_num / f_num) / (non_m_num / non_f_num), 2)
    
    top_odds = dict(sorted(odds_ratio.items(), key=itemgetter(1), reverse=True)[:topk])
    bottom_odds = dict(sorted(odds_ratio.items(), key=itemgetter(1))[:topk])
    return top_odds, bottom_odds
