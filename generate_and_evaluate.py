import os
import sys
from datetime import datetime
from metrics.cal_odds_ratio import process_stories_odd_ratio
from metrics.analyse_sttr_mtld_n_gram_diversity_inverse_homogenization_sentiment import analyze_stories, save_results_to_file
from plot.draw_odds_ratio import plot_odds_ratios
from plot.draw_all_metrics import generate_plots
from storyGeneration_llama import generate_stories

def main(model_name, num_per_gender, top_k, model_generate_config=None, cultures=None):
    # Step 1: 生成故事
    sanitized_model_name = model_name.replace("/", "_")  # 替换/以避免路径问题
    story_output_dir = f"{sanitized_model_name}_story"

    print(f"Generating stories using model: {model_name}...")
    if cultures is None:
        cultures = ['Chinese', 'Portuguese', 'Spanish', 'Arabic']  # 默认传入所有四个文化
    generate_stories(model_name, num_per_gender=num_per_gender, output_dir=story_output_dir, model_generate_config=model_generate_config, cultures=cultures)
    print(f"Stories generated and saved to {story_output_dir}")

    # Step 2: 设置结果输出路径
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join('results', sanitized_model_name, timestamp)
    os.makedirs(results_dir, exist_ok=True)

    # 定义输入和输出路径
    odds_ratio_results_file = os.path.join(results_dir, 'odds_ratio_results.json')
    odds_ratio_plot_file = os.path.join(results_dir, 'odds_ratios_plot.png')
    analysis_results_file = os.path.join(results_dir, 'analysis_results.json')
    metrics_plots_output_dir = os.path.join(results_dir, 'metrics_plots')

    # 确保绘图输出目录存在
    os.makedirs(metrics_plots_output_dir, exist_ok=True)

    # Step 3: 处理故事数据，生成odds ratio的结果文件
    print("Processing stories for odds ratio...")
    process_stories_odd_ratio(story_output_dir, output_file=odds_ratio_results_file)
    print(f"Odds ratio results saved to {odds_ratio_results_file}")

    # Step 4: 绘制odds ratio的图
    print("Plotting odds ratios...")
    plot_odds_ratios(odds_ratio_results_file, odds_ratio_plot_file)
    print(f"Odds ratio plot saved to {odds_ratio_plot_file}")

    # Step 5: 分析故事数据，生成分析结果文件
    print("Analyzing stories...")
    analysis_results = analyze_stories(story_output_dir, top_k)
    save_results_to_file(analysis_results_file, analysis_results)
    print(f"Analysis results saved to {analysis_results_file}")

    # Step 6: 根据分析结果绘制所有指标的图
    print("Generating metric plots...")
    metrics_to_plot = ['normalized_ttr', 'mtld_score', 'polarity', 'subjectivity', 'positive_ratio', 'negative_ratio']
    generate_plots(analysis_results_file, metrics_to_plot, metrics_plots_output_dir)
    print(f"Metric plots saved to {metrics_plots_output_dir}")

    print("All tasks completed successfully!")

if __name__ == '__main__':
    # 检查是否提供了模型名称参数
    model_name='meta-llama/Llama-3.1-8B-Instruct'
    model_generate_config = {'max_new_tokens': 2000,
                            'temperature': 1.0,
                            'top_p': 1.0,
                            'do_sample': True}
    
    num_per_gender=30  # 给定文化和性别，生成多少故事
    top_k=5  #每个story取出排名前top_k的positive词和negative词
    cultures=['Chinese', 'Portuguese', 'Spanish', 'Arabic']  # 默认传入所有四个文化

    main(model_name, num_per_gender, top_k, model_generate_config=model_generate_config, cultures=cultures)
