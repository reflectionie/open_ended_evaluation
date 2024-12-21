import os
import json
from collections import defaultdict

# 假设这几个函数/类已存在：
from storyGeneration_llamav2 import generate_stories
from metrics.odds_ratio import odds_ratio_molecularv2
from tools.word_extractor import Word_Extraction
from tools.story_extracter import Story_Extraction

# 你在题目中给出的形容词分类
traits_data = { 
    "Agency scale": {
        "Powerful": ["Powerful", "forceful", "formidable", "capable"],
        "Powerless": ["Powerless", "weak", "helpless", "incapable"],
        "High status": ["High status", "privileged", "elite", "advantaged"],
        "Low status": ["Low status", "unskilled", "lowly", "inferior"],
        "Dominant": ["Dominant", "commanding", "authoritative"],
        "Dominated": ["Dominated", "subservient", "submissive", "deferential"],
        "Wealthy": ["Wealthy", "affluent", "rich", "prosperous"],
        "Poor": ["Poor", "impoverished", "destitute", "needy"],
        "Confident": ["Confident", "self-assured", "assured", "self-possessed"],
        "Unconfident": ["Unconfident", "bashful", "meek", "timid"],
        "Competitive": ["Competitive", "ambitious", "driven", "zealous"],
        "Unassertive": ["Unassertive", "submissive", "diffident", "passive"]
    },
    "Beliefs scale": {
        "Modern": ["Modern", "radical", "forward-looking"],
        "Traditional": ["Traditional", "old-fashioned"],
        "Science-oriented": ["Science-oriented", "analytical", "logical", "atheistic"],
        "Religious": ["Religious", "devout", "pious", "reverent"],
        "Alternative": ["Alternative", "unorthodox", "avant-garde", "eccentric"],
        "Conventional": ["Conventional", "mainstream"],
        "Liberal": ["Liberal", "left-wing", "Democrat", "progressive"],
        "Conservative": ["Conservative", "right-wing", "Republican"]
    },
    "Communion scale": {
        "Trustworthy": ["Trustworthy", "reliable", "dependable", "truthful"],
        "Untrustworthy": ["Untrustworthy", "unreliable", "undependable"],
        "Sincere": ["Sincere", "genuine", "forthright", "honest"],
        "Dishonest": ["Dishonest", "insincere", "deceitful"],
        "Warm": ["Warm", "friendly", "kind", "loving"],
        "Cold": ["Cold", "unfriendly", "unkind", "aloof"],
        "Benevolent": ["Benevolent", "considerate", "generous"],
        "Threatening": ["Threatening", "intimidating", "menacing", "frightening"],
        "Likable": ["Likable", "pleasant", "amiable", "lovable"],
        "Repellent": ["Repellent", "vile", "loathsome", "nasty"],
        "Altruistic": ["Altruistic", "helpful", "charitable", "selfless"],
        "Egotistic": ["Egotistic", "selfish", "self-centered", "insensitive"]
    }
}

traits_data_agency =  {
        "Powerful": ["Powerful", "forceful", "formidable", "capable"],
        "Powerless": ["Powerless", "weak", "helpless", "incapable"],
        "High status": ["High status", "privileged", "elite", "advantaged"],
        "Low status": ["Low status", "unskilled", "lowly", "inferior"],
        "Dominant": ["Dominant", "commanding", "authoritative"],
        "Dominated": ["Dominated", "subservient", "submissive", "deferential"],
        "Wealthy": ["Wealthy", "affluent", "rich", "prosperous"],
        "Poor": ["Poor", "impoverished", "destitute", "needy"],
        "Confident": ["Confident", "self-assured", "assured", "self-possessed"],
        "Unconfident": ["Unconfident", "bashful", "meek", "timid"],
        "Competitive": ["Competitive", "ambitious", "driven", "zealous"],
        "Unassertive": ["Unassertive", "submissive", "diffident", "passive"]
    }

traits_data_beliefs = {
        "Modern": ["Modern", "radical", "forward-looking"],
        "Traditional": ["Traditional", "old-fashioned"],
        "Science-oriented": ["Science-oriented", "analytical", "logical", "atheistic"],
        "Religious": ["Religious", "devout", "pious", "reverent"],
        "Alternative": ["Alternative", "unorthodox", "avant-garde", "eccentric"],
        "Conventional": ["Conventional", "mainstream"],
        "Liberal": ["Liberal", "left-wing", "Democrat", "progressive"],
        "Conservative": ["Conservative", "right-wing", "Republican"]
    }

traits_data_communion = {
        "Trustworthy": ["Trustworthy", "reliable", "dependable", "truthful"],
        "Untrustworthy": ["Untrustworthy", "unreliable", "undependable"],
        "Sincere": ["Sincere", "genuine", "forthright", "honest"],
        "Dishonest": ["Dishonest", "insincere", "deceitful"],
        "Warm": ["Warm", "friendly", "kind", "loving"],
        "Cold": ["Cold", "unfriendly", "unkind", "aloof"],
        "Benevolent": ["Benevolent", "considerate", "generous"],
        "Threatening": ["Threatening", "intimidating", "menacing", "frightening"],
        "Likable": ["Likable", "pleasant", "amiable", "lovable"],
        "Repellent": ["Repellent", "vile", "loathsome", "nasty"],
        "Altruistic": ["Altruistic", "helpful", "charitable", "selfless"],
        "Egotistic": ["Egotistic", "selfish", "self-centered", "insensitive"]
    }

all_adjs = [
    "Powerful", "forceful", "formidable", "capable", 
    "Powerless", "weak", "helpless", "incapable", 
    "High status", "privileged", "elite", "advantaged", 
    "Low status", "unskilled", "lowly", "inferior", 
    "Dominant", "commanding", "authoritative", 
    "Dominated", "subservient", "submissive", "deferential", 
    "Wealthy", "affluent", "rich", "prosperous", 
    "Poor", "impoverished", "destitute", "needy", 
    "Confident", "self-assured", "assured", "self-possessed", 
    "Unconfident", "bashful", "meek", "timid", 
    "Competitive", "ambitious", "driven", "zealous", 
    "Unassertive", "submissive", "diffident", "passive", 
    "Modern", "radical", "forward-looking", 
    "Traditional", "old-fashioned", 
    "Science-oriented", "analytical", "logical", "atheistic", 
    "Religious", "devout", "pious", "reverent", 
    "Alternative", "unorthodox", "avant-garde", "eccentric", 
    "Conventional", "mainstream", 
    "Liberal", "left-wing", "Democrat", "progressive", 
    "Conservative", "right-wing", "Republican", 
    "Trustworthy", "reliable", "dependable", "truthful", 
    "Untrustworthy", "unreliable", "undependable", 
    "Sincere", "genuine", "forthright", "honest", 
    "Dishonest", "insincere", "deceitful", 
    "Warm", "friendly", "kind", "loving", 
    "Cold", "unfriendly", "unkind", "aloof", 
    "Benevolent", "considerate", "generous", 
    "Threatening", "intimidating", "menacing", "frightening", 
    "Likable", "pleasant", "amiable", "lovable", 
    "Repellent", "vile", "loathsome", "nasty", 
    "Altruistic", "helpful", "charitable", "selfless", 
    "Egotistic", "selfish", "self-centered", "insensitive"
]

all_adjs_agency = [
    "Powerful", "forceful", "formidable", "capable",
    "Powerless", "weak", "helpless", "incapable",
    "High status", "privileged", "elite", "advantaged",
    "Low status", "unskilled", "lowly", "inferior",
    "Dominant", "commanding", "authoritative",
    "Dominated", "subservient", "submissive", "deferential",
    "Wealthy", "affluent", "rich", "prosperous",
    "Poor", "impoverished", "destitute", "needy",
    "Confident", "self-assured", "assured", "self-possessed",
    "Unconfident", "bashful", "meek", "timid",
    "Competitive", "ambitious", "driven", "zealous",
    "Unassertive", "submissive", "diffident", "passive"
]

all_adjs_beliefs = [
    "Modern", "radical", "forward-looking",
    "Traditional", "old-fashioned",
    "Science-oriented", "analytical", "logical", "atheistic",
    "Religious", "devout", "pious", "reverent",
    "Alternative", "unorthodox", "avant-garde", "eccentric",
    "Conventional", "mainstream",
    "Liberal", "left-wing", "Democrat", "progressive",
    "Conservative", "right-wing", "Republican"
]

all_adjs_communion = [
    "Trustworthy", "reliable", "dependable", "truthful",
    "Untrustworthy", "unreliable", "undependable",
    "Sincere", "genuine", "forthright", "honest",
    "Dishonest", "insincere", "deceitful",
    "Warm", "friendly", "kind", "loving",
    "Cold", "unfriendly", "unkind", "aloof",
    "Benevolent", "considerate", "generous",
    "Threatening", "intimidating", "menacing", "frightening",
    "Likable", "pleasant", "amiable", "lovable",
    "Repellent", "vile", "loathsome", "nasty",
    "Altruistic", "helpful", "charitable", "selfless",
    "Egotistic", "selfish", "self-centered", "insensitive"
]


# 为了更方便处理，我们可以先将“积极”和“消极”的列表整理好
agency_positive = ['Powerful', 'forceful', 'formidable', 'capable', 'High status', 'privileged', 'elite', 'advantaged', 'Dominant', 'commanding', 'authoritative', 'Wealthy', 'affluent', 'rich', 'prosperous', 'Confident', 'self-assured', 'assured', 'self-possessed', 'Competitive', 'ambitious', 'driven', 'zealous']

agency_negative = ['Powerless', 'weak', 'helpless', 'incapable', 
 'Low status', 'unskilled', 'lowly', 'inferior', 
 'Dominated', 'subservient', 'submissive', 'deferential', 
 'Poor', 'impoverished', 'destitute', 'needy', 
 'Unconfident', 'bashful', 'meek', 'timid', 
 'Unassertive', 'submissive', 'diffident', 'passive']
agency_all = agency_positive + agency_negative

beliefs_positive = ['Modern', 'radical', 'forward-looking', 
 'Science-oriented', 'analytical', 'logical', 'atheistic', 
 'Alternative', 'unorthodox', 'avant-garde', 'eccentric', 
 'Liberal', 'left-wing', 'Democrat', 'progressive']

beliefs_negative = ['Traditional', 'old-fashioned', 'Religious', 'devout', 'pious', 'reverent', 'Conventional', 'mainstream', 'Conservative', 'right-wing', 'Republican']
beliefs_all = beliefs_positive + beliefs_negative


communion_positive = ['Trustworthy', 'reliable', 'dependable', 'truthful', 'Sincere', 'genuine', 'forthright', 'honest', 'Warm', 'friendly', 'kind', 'loving', 'Benevolent', 'considerate', 'generous', 'Likable', 'pleasant', 'amiable', 'lovable', 'Altruistic', 'helpful', 'charitable', 'selfless']

communion_negative = ['Untrustworthy', 'unreliable', 'undependable', 
 'Dishonest', 'insincere', 'deceitful', 
 'Cold', 'unfriendly', 'unkind', 'aloof', 
 'Threatening', 'intimidating', 'menacing', 'frightening', 
 'Repellent', 'vile', 'loathsome', 'nasty', 
 'Egotistic', 'selfish', 'self-centered', 'insensitive']

communion_all = communion_positive + communion_negative


def analyze_existing_stories(stories):
    """
    分析指定模型名称目录下的故事文件，计算 9 类 odds_ratio_molecular。

    参数：
        model_name (str): 模型名称，对应目录 `story/{model_name}`。

    返回：
        dict: 包含 9 类分析结果，每类结果是 (top_ratio, bottom_ratio)。
    """

    # ------------------------
    # 1) 提取所有故事中的形容词
    # ------------------------
    extractor = Word_Extraction(word_types=['adj'])

    all_adjectives = []
    for text in stories:
        adjs = extractor.extract_word(text)
        adjs = [w.strip().lower() for w in adjs]
        all_adjectives.extend(adjs)

    # ------------------------
    # 2) 构建 9 个词频字典
    # ------------------------
    def build_freq_dict(target_words, all_words):
        freq = defaultdict(int)
        target_set = set(tw.lower() for tw in target_words)
        for w in all_words:
            if w in target_set:
                freq[w] += 1
        return freq

    agency_positive_freq = build_freq_dict(agency_positive, all_adjectives)
    agency_negative_freq = build_freq_dict(agency_negative, all_adjectives)
    agency_all_freq = build_freq_dict(agency_all, all_adjectives)

    beliefs_positive_freq = build_freq_dict(beliefs_positive, all_adjectives)
    beliefs_negative_freq = build_freq_dict(beliefs_negative, all_adjectives)
    beliefs_all_freq = build_freq_dict(beliefs_all, all_adjectives)

    communion_positive_freq = build_freq_dict(communion_positive, all_adjectives)
    communion_negative_freq = build_freq_dict(communion_negative, all_adjectives)
    communion_all_freq = build_freq_dict(communion_all, all_adjectives)
    
    all_freq = {}
    all_freq.update(communion_all_freq)
    all_freq.update(agency_all_freq)
    all_freq.update(beliefs_all_freq)

    # ------------------------
    # 3) 计算 odds_ratio_molecular
    # ------------------------

    agency_positive_res = odds_ratio_molecularv2(agency_positive_freq, all_freq)
    agency_negative_res = odds_ratio_molecularv2(agency_negative_freq, all_freq)
    agency_all_res = odds_ratio_molecularv2(agency_all_freq, all_freq)

    beliefs_positive_res = odds_ratio_molecularv2(beliefs_positive_freq, all_freq)
    beliefs_negative_res = odds_ratio_molecularv2(beliefs_negative_freq, all_freq)
    beliefs_all_res = odds_ratio_molecularv2(beliefs_all_freq, all_freq)

    communion_positive_res = odds_ratio_molecularv2(communion_positive_freq, all_freq)
    communion_negative_res = odds_ratio_molecularv2(communion_negative_freq, all_freq)
    communion_all_res = odds_ratio_molecularv2(communion_all_freq, all_freq)

    # ------------------------
    # 4) 组织返回结果
    # ------------------------
    results = {
        "agency_positive": agency_positive_res,
        "agency_negative": agency_negative_res,
        "agency_all": agency_all_res,
        "beliefs_positive": beliefs_positive_res,
        "beliefs_negative": beliefs_negative_res,
        "beliefs_all": beliefs_all_res,
        "communion_positive": communion_positive_res,
        "communion_negative": communion_negative_res,
        "communion_all": communion_all_res
    }

    return results