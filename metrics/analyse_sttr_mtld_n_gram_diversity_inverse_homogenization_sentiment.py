import os
import json
from collections import defaultdict
from tqdm import tqdm
from metrics.cal_STTR import calculate_normalized_ttr
from metrics.cal_MTLD import calculate_mtld
from metrics.cal_n_gram_diversity_or_inverse_homogenization import compute_n_gram_diversity
from metrics.cal_sentiment_score import analyze_sentiment
from metrics.cal_words_ratio import analyze_positive_words, analyze_negative_words, get_top_k_words

def analyze_story(story_text, top_k):
    results = {}
    results['normalized_ttr'] = calculate_normalized_ttr(story_text)
    results['mtld_score'] = calculate_mtld(story_text)
    n_gram_diversity, _ = compute_n_gram_diversity(story_text)
    results['n_gram_diversity'] = n_gram_diversity
    polarity, subjectivity = analyze_sentiment(story_text)
    results['polarity'] = polarity
    results['subjectivity'] = subjectivity
    pos_analysis = analyze_positive_words(story_text)
    neg_analysis = analyze_negative_words(story_text)
    results.update(pos_analysis)
    results.update(neg_analysis)
    top_positive_words, top_negative_words = get_top_k_words(story_text, top_k=top_k)
    results['top_positive_words'] = top_positive_words
    results['top_negative_words'] = top_negative_words
    return results

def process_folder(root_folder, top_k):
    results_by_culture_gender = defaultdict(lambda: defaultdict(list))
    for culture in tqdm(os.listdir(root_folder), desc="Cultures"):
        culture_path = os.path.join(root_folder, culture)
        if not os.path.isdir(culture_path):
            continue
        for gender in tqdm(os.listdir(culture_path), desc=f"Genders in {culture}", leave=False):
            gender_path = os.path.join(culture_path, gender)
            if not os.path.isdir(gender_path):
                continue
            for filename in tqdm(os.listdir(gender_path), desc=f"Files in {gender}", leave=False):
                if filename.endswith('.json'):
                    file_path = os.path.join(gender_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        story_text = data.get('story', '')
                        if story_text:
                            analysis_results = analyze_story(story_text, top_k)
                            results_by_culture_gender[culture][gender].append(analysis_results)
    return results_by_culture_gender

def get_top_k_from_set(word_set, top_k, descending=True):
    sorted_words = sorted(word_set, key=lambda x: x[1], reverse=descending)
    return sorted_words[:top_k]

def calculate_averages(results_by_culture_gender, top_k):
    averages_by_culture_gender = {}
    for culture, genders in results_by_culture_gender.items():
        averages_by_culture_gender[culture] = {}
        for gender, results in genders.items():
            if not results:
                continue
            average_results = defaultdict(float)
            top_positive_words_set = set()
            top_negative_words_set = set()
            num_stories = len(results)
            for result in results:
                for key, value in result.items():
                    if isinstance(value, (int, float)):
                        average_results[key] += value
                    elif key == 'top_positive_words':
                        top_positive_words_set.update(value)
                    elif key == 'top_negative_words':
                        top_negative_words_set.update(value)
            for key in average_results:
                average_results[key] /= num_stories
            average_results['top_positive_words'] = get_top_k_from_set(top_positive_words_set, top_k, descending=True)
            average_results['top_negative_words'] = get_top_k_from_set(top_negative_words_set, top_k, descending=False)
            averages_by_culture_gender[culture][gender] = dict(average_results)
    return averages_by_culture_gender

def calculate_additional_averages(averages_by_culture_gender, top_k):
    averages_by_culture = {}
    for culture, genders in averages_by_culture_gender.items():
        combined_results = defaultdict(float)
        combined_positive_words = set()
        combined_negative_words = set()
        total_counts = defaultdict(int)
        for gender, averages in genders.items():
            for key, value in averages.items():
                if isinstance(value, (int, float)):
                    combined_results[key] += value
                    total_counts[key] += 1
                elif key == 'top_positive_words':
                    combined_positive_words.update(value)
                elif key == 'top_negative_words':
                    combined_negative_words.update(value)
        averages_by_culture[culture] = {key: combined_results[key] / total_counts[key] for key in combined_results}
        averages_by_culture[culture]['top_positive_words'] = get_top_k_from_set(combined_positive_words, top_k)
        averages_by_culture[culture]['top_negative_words'] = get_top_k_from_set(combined_negative_words, top_k)
    averages_by_gender = defaultdict(lambda: defaultdict(float))
    combined_positive_words_by_gender = defaultdict(set)
    combined_negative_words_by_gender = defaultdict(set)
    counts_by_gender = defaultdict(lambda: defaultdict(int))
    for culture, genders in averages_by_culture_gender.items():
        for gender, averages in genders.items():
            for key, value in averages.items():
                if isinstance(value, (int, float)):
                    averages_by_gender[gender][key] += value
                    counts_by_gender[gender][key] += 1
                elif key == 'top_positive_words':
                    combined_positive_words_by_gender[gender].update(value)
                elif key == 'top_negative_words':
                    combined_negative_words_by_gender[gender].update(value)
    for gender in averages_by_gender:
        for key in averages_by_gender[gender]:
            averages_by_gender[gender][key] /= counts_by_gender[gender][key]
        averages_by_gender[gender]['top_positive_words'] = get_top_k_from_set(combined_positive_words_by_gender[gender], top_k)
        averages_by_gender[gender]['top_negative_words'] = get_top_k_from_set(combined_negative_words_by_gender[gender], top_k)
    return averages_by_culture, averages_by_gender

def save_results_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def analyze_stories(root_folder, top_k):
    results_by_culture_gender = process_folder(root_folder, top_k)
    averages_by_culture_gender = calculate_averages(results_by_culture_gender, top_k)
    averages_by_culture, averages_by_gender = calculate_additional_averages(averages_by_culture_gender, top_k)
    all_results = {
        "averages_by_culture_gender": averages_by_culture_gender,
        "averages_by_culture": averages_by_culture,
        "averages_by_gender": averages_by_gender
    }
    return all_results

# Example usage
if __name__ == "__main__":
    root_folder = 'story'
    top_k = 5  # You can now set this to any value you want
    analysis_results = analyze_stories(root_folder, top_k)
    save_results_to_file('analysis_results.json', analysis_results)
