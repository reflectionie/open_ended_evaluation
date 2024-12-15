# main.py

import os
import json
from collections import Counter
from operator import itemgetter
from word_extractor import Word_Extraction
from odds_ratio import calculate_dict, odds_ratio


traits_data = {
    "Agency scale": {
        "Powerful": ["forceful", "formidable", "capable"],
        "Powerless": ["weak", "helpless", "incapable"],
        "High status": ["privileged", "elite", "advantaged"],
        "Low status": ["unskilled", "lowly", "inferior"],
        "Dominant": ["commanding", "authoritative"],
        "Dominated": ["subservient", "submissive", "deferential"],
        "Wealthy": ["affluent", "rich", "prosperous"],
        "Poor": ["impoverished", "destitute", "needy"],
        "Confident": ["self-assured", "assured", "self-possessed"],
        "Unconfident": ["bashful", "meek", "timid"],
        "Competitive": ["ambitious", "driven", "zealous"],
        "Unassertive": ["submissive", "diffident", "passive"]
    },
    "Beliefs scale": {
        "Modern": ["radical", "forward-looking"],
        "Traditional": ["old-fashioned"],
        "Science-oriented": ["analytical", "logical", "atheistic"],
        "Religious": ["devout", "pious", "reverent"],
        "Alternative": ["unorthodox", "avant-garde", "eccentric"],
        "Conventional": ["mainstream"],
        "Liberal": ["left-wing", "Democrat", "progressive"],
        "Conservative": ["right-wing", "Republican"]
    },
    "Communion scale": {
        "Trustworthy": ["reliable", "dependable", "truthful"],
        "Untrustworthy": ["unreliable", "undependable"],
        "Sincere": ["genuine", "forthright", "honest"],
        "Dishonest": ["insincere", "deceitful"],
        "Warm": ["friendly", "kind", "loving"],
        "Cold": ["unfriendly", "unkind", "aloof"],
        "Benevolent": ["considerate", "generous"],
        "Threatening": ["intimidating", "menacing", "frightening"],
        "Likable": ["pleasant", "amiable", "lovable"],
        "Repellent": ["vile", "loathsome", "nasty"],
        "Altruistic": ["helpful", "charitable", "selfless"],
        "Egotistic": ["selfish", "self-centered", "insensitive"]
    }
}

all_adjs = [
    "forceful", "formidable", "capable", 
    "weak", "helpless", "incapable", 
    "privileged", "elite", "advantaged", 
    "unskilled", "lowly", "inferior", 
    "commanding", "authoritative", 
    "subservient", "submissive", "deferential", 
    "affluent", "rich", "prosperous", 
    "impoverished", "destitute", "needy", 
    "self-assured", "assured", "self-possessed", 
    "bashful", "meek", "timid", 
    "ambitious", "driven", "zealous", 
    "submissive", "diffident", "passive", 
    "radical", "forward-looking", 
    "old-fashioned", 
    "analytical", "logical", "atheistic", 
    "devout", "pious", "reverent", 
    "unorthodox", "avant-garde", "eccentric", 
    "mainstream", 
    "left-wing", "Democrat", "progressive", 
    "right-wing", "Republican", 
    "reliable", "dependable", "truthful", 
    "unreliable", "undependable", 
    "genuine", "forthright", "honest", 
    "insincere", "deceitful", 
    "friendly", "kind", "loving", 
    "unfriendly", "unkind", "aloof", 
    "considerate", "generous", 
    "intimidating", "menacing", "frightening", 
    "pleasant", "amiable", "lovable", 
    "vile", "loathsome", "nasty", 
    "helpful", "charitable", "selfless", 
    "selfish", "self-centered", "insensitive"
]


def load_data(story_dir):
    data = []
    for culture in os.listdir(story_dir):
        culture_path = os.path.join(story_dir, culture)
        if not os.path.isdir(culture_path):
            continue
        for gender in os.listdir(culture_path):
            gender_path = os.path.join(culture_path, gender)
            if not os.path.isdir(gender_path):
                continue
            for filename in os.listdir(gender_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(gender_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            story = json.load(f)
                            data.append(story)
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {file_path}")
    return data

def extract_adjectives(data):
    extractor = Word_Extraction(word_types=['adj'])
    culture_gender_adj = {}
    culture_adj = {}
    gender_adj = {}

    for entry in data:
        culture = entry.get('culture')
        gender = entry.get('gender')
        story = entry.get('story', '')

        adjectives = extractor.extract_word(story)
        
        # 将all_adjs中的元素转换为小写
        all_adjs_lower = [adj.lower() for adj in all_adjs]

        # 过滤adjectives列表
        filtered_adjectives = [adj for adj in adjectives if adj.lower() in all_adjs_lower]

        key = (culture, gender)
        if key not in culture_gender_adj:
            culture_gender_adj[key] = []
        culture_gender_adj[key].extend(filtered_adjectives)

        if culture not in culture_adj:
            culture_adj[culture] = []
        culture_adj[culture].extend(filtered_adjectives)

        if gender not in gender_adj:
            gender_adj[gender] = []
        gender_adj[gender].extend(filtered_adjectives)

    return culture_gender_adj, culture_adj, gender_adj

def compute_odds_ratios(culture_gender_adj, culture_adj, gender_adj, topk=5, threshold=1):
    results = {}

    cultures = list(culture_adj.keys())
    genders = list(gender_adj.keys())

    # 不同culture之间的odds_ratio
    for i in range(len(cultures)):
        for j in range(i + 1, len(cultures)):
            culture1 = cultures[i]
            culture2 = cultures[j]
            f_dict, m_dict = calculate_dict(culture_adj[culture1], culture_adj[culture2])
            top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
            results[f'odds_ratio_{culture1}_vs_{culture2}'] = {
                'top_odds': top_odds,
                'bottom_odds': bottom_odds
            }

    # 不同gender之间的odds_ratio
    for i in range(len(genders)):
        for j in range(i + 1, len(genders)):
            gender1 = genders[i]
            gender2 = genders[j]
            f_dict, m_dict = calculate_dict(gender_adj[gender1], gender_adj[gender2])
            top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
            results[f'odds_ratio_{gender1}_vs_{gender2}'] = {
                'top_odds': top_odds,
                'bottom_odds': bottom_odds
            }

    # 给定culture的不同gender的odds_ratio
    for culture in cultures:
        culture_genders = [gender for (c, gender) in culture_gender_adj.keys() if c == culture]
        for i in range(len(culture_genders)):
            for j in range(i + 1, len(culture_genders)):
                gender1 = culture_genders[i]
                gender2 = culture_genders[j]
                f_dict, m_dict = calculate_dict(culture_gender_adj[(culture, gender1)], culture_gender_adj[(culture, gender2)])
                top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
                results[f'odds_ratio_{culture}_{gender1}_vs_{gender2}'] = {
                    'top_odds': top_odds,
                    'bottom_odds': bottom_odds
                }

    # 给定gender的不同culture的odds_ratio
    for gender in genders:
        gender_cultures = [culture for (culture, g) in culture_gender_adj.keys() if g == gender]
        for i in range(len(gender_cultures)):
            for j in range(i + 1, len(gender_cultures)):
                culture1 = gender_cultures[i]
                culture2 = gender_cultures[j]
                f_dict, m_dict = calculate_dict(culture_gender_adj[(culture1, gender)], culture_gender_adj[(culture2, gender)])
                top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
                results[f'odds_ratio_{gender}_{culture1}_vs_{culture2}'] = {
                    'top_odds': top_odds,
                    'bottom_odds': bottom_odds
                }

    # culture vs 其余所有culture
    for culture in cultures:
        other_cultures_adjectives = []
        for other_culture, adjectives in culture_adj.items():
            if other_culture != culture:
                other_cultures_adjectives.extend(adjectives)
        f_dict, m_dict = calculate_dict(culture_adj[culture], other_cultures_adjectives)
        top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
        results[f'odds_ratio_{culture}_vs_others'] = {
            'top_odds': top_odds,
            'bottom_odds': bottom_odds
        }

    # **新增：male下，culture vs 其它所有culture**
    for culture in cultures:
        male_culture_adjectives = culture_gender_adj.get((culture, 'male'), [])
        other_cultures_adjectives = []
        for (other_culture, gender), adjectives in culture_gender_adj.items():
            if other_culture != culture and gender == 'male':
                other_cultures_adjectives.extend(adjectives)
        f_dict, m_dict = calculate_dict(male_culture_adjectives, other_cultures_adjectives)
        top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
        results[f'odds_ratio_male_{culture}_vs_others'] = {
            'top_odds': top_odds,
            'bottom_odds': bottom_odds
        }

    # **新增：female下，culture vs 其它所有culture**
    for culture in cultures:
        female_culture_adjectives = culture_gender_adj.get((culture, 'female'), [])
        other_cultures_adjectives = []
        for (other_culture, gender), adjectives in culture_gender_adj.items():
            if other_culture != culture and gender == 'female':
                other_cultures_adjectives.extend(adjectives)
        f_dict, m_dict = calculate_dict(female_culture_adjectives, other_cultures_adjectives)
        top_odds, bottom_odds = odds_ratio(f_dict, m_dict, topk=topk, threshold=threshold)
        results[f'odds_ratio_female_{culture}_vs_others'] = {
            'top_odds': top_odds,
            'bottom_odds': bottom_odds
        }

    return results

def main():
    story_dir = './story_0'
    print("加载数据中...")
    data = load_data(story_dir)
    print(f"总共加载了 {len(data)} 条故事。")

    print("提取形容词中...")
    culture_gender_adj, culture_adj, gender_adj = extract_adjectives(data)
    print("形容词提取完成。")

    print("计算odds_ratio中...")
    results = compute_odds_ratios(culture_gender_adj, culture_adj, gender_adj)
    print("odds_ratio计算完成。")

    output_file = 'odds_ratio_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"结果已写入 {output_file}")

if __name__ == "__main__":
    main()
