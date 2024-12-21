import os
from datetime import datetime
from metrics.cal_odds_ratio import process_stories_odd_ratio
from metrics.analyse_sttr_mtld_n_gram_diversity_inverse_homogenization_sentiment import analyze_stories, save_results_to_file
from plot.draw_odds_ratio import plot_odds_ratios
from plot.draw_all_metrics import generate_plots

def main():
    # 假设故事已经生成，指定故事目录
    story_output_dir = "generated_stories/Arabic/female"  # 替换为实际的故事目录
    if not os.path.exists(story_output_dir):
        print(f"Error: Story directory '{story_output_dir}' does not exist.")
        return

    # 设置结果输出路径
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join('results', 'evaluate_results', timestamp)
    os.makedirs(results_dir, exist_ok=True)

    # 定义输入和输出路径
    odds_ratio_results_file = os.path.join(results_dir, 'odds_ratio_results.json')
    odds_ratio_plot_file = os.path.join(results_dir, 'odds_ratios_plot.png')
    analysis_results_file = os.path.join(results_dir, 'analysis_results.json')
    metrics_plots_output_dir = os.path.join(results_dir, 'metrics_plots')

    # 确保绘图输出目录存在
    os.makedirs(metrics_plots_output_dir, exist_ok=True)

    # Step 1: 处理故事数据，生成 odds ratio 的结果文件
    print("Processing stories for odds ratio...")
    process_stories_odd_ratio(story_output_dir, output_file=odds_ratio_results_file)
    print(f"Odds ratio results saved to {odds_ratio_results_file}")

    # Step 2: 绘制 odds ratio 的图
    print("Plotting odds ratios...")
    plot_odds_ratios(odds_ratio_results_file, odds_ratio_plot_file)
    print(f"Odds ratio plot saved to {odds_ratio_plot_file}")

    # Step 3: 分析故事数据，生成分析结果文件
    print("Analyzing stories...")
    analysis_results = analyze_stories(story_output_dir)
    save_results_to_file(analysis_results_file, analysis_results)
    print(f"Analysis results saved to {analysis_results_file}")

    # Step 4: 根据分析结果绘制所有指标的图
    print("Generating metric plots...")
    metrics_to_plot = ['normalized_ttr', 'mtld_score', 'polarity', 'subjectivity', 'positive_ratio', 'negative_ratio']
    generate_plots(analysis_results_file, metrics_to_plot, metrics_plots_output_dir)
    print(f"Metric plots saved to {metrics_plots_output_dir}")

    print("All tasks completed successfully!")

if __name__ == '__main__':
    main()
