import os
import json
import argparse
from storyGeneration_llamav2 import generate_stories
from tools.story_extracter import Story_Extraction
from metrics.cal_odds_ratiov2 import analyze_existing_stories
from metrics.cal_green_red import evaluate_stories
import pandas as pd

# 确保存储路径存在
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 将字典写入 JSON 文件
def save_dict_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 将字典写入 Excel 文件（所有值写在一行，表头为另一行）
def save_dict_to_excel_row(data, file_path):
    df = pd.DataFrame([data])
    df.to_excel(file_path, index=False)

# 主函数
def main(args):
    model_name = args.model_name
    cultures = args.cultures
    use_generate_stories = args.generate

    num_per_gender = 10
    model_generate_config = {
        'max_new_tokens': 1000,
        'temperature': 1.0,
        'top_p': 1.0,
        'do_sample': True
    }

    base_dir = f"./story/{model_name}"

    if use_generate_stories:
        print("Generating stories...")
        generate_stories(
            model_name=model_name,
            num_per_gender=num_per_gender,
            output_dir="./story",
            model_generate_config=model_generate_config,
            cultures=cultures
        )
    else:
        print("Skipping story generation. Reading existing stories.")

    # 提取所有故事
    print("Extracting stories...")
    stories = Story_Extraction(base_dir)
    print(f"Extracted {len(stories)} stories.")

    # 分析故事的Odds Ratio
    print("Analyzing stories (Odds Ratio)...")
    odds_ratio_results = analyze_existing_stories(stories)
    print("Odds Ratio Analysis Results:")
    print(odds_ratio_results)

    # 评估故事的Green/Red分数
    print("Evaluating stories (Green/Red scores)...")
    evaluation_results = evaluate_stories(stories)
    print("Evaluation Results:")
    print(evaluation_results)

    results_folder = "results"
    save_path = os.path.join(results_folder, model_name)

    ensure_directory_exists(save_path)

    # 写入 JSON
    json_file_path = os.path.join(save_path, "odds_ratio_results.json")
    save_dict_to_json(odds_ratio_results, json_file_path)

    # 写入 Excel
    excel_file_path = os.path.join(save_path, "evaluation_results.xlsx")
    save_dict_to_excel_row(evaluation_results, excel_file_path)

    print(f"Results saved to: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and evaluate stories.")
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model to use.")
    parser.add_argument("--cultures", type=str, nargs='+', required=True, help="List of cultures to generate stories for.")
    parser.add_argument("--generate", action='store_true', help="Flag to indicate whether to generate new stories.")

    args = parser.parse_args()

    main(args)
