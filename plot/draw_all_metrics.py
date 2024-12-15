import json
import matplotlib.pyplot as plt
import numpy as np

def generate_plots(file_path, attributes, output_dir):
    """
    从指定的 JSON 文件读取数据，并生成相关的图表。

    :param file_path: 输入的 JSON 文件路径
    :param attributes: 需要绘制的属性列表
    :param output_dir: 输出图表的目录
    """
    # 读取 JSON 文件
    with open(file_path, 'r') as f:
        data = json.load(f)

    # 处理的三个部分
    sections = {
        'averages_by_culture_gender': data.get('averages_by_culture_gender', {}),
        'averages_by_culture': data.get('averages_by_culture', {}),
        'averages_by_gender': data.get('averages_by_gender', {})
    }

    def plot_averages(data, attributes, x_label, title, save_path):
        """绘制每个部分的子图，每个子图显示一个属性的变化"""
        num_attributes = len(attributes)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # 2x3 网格
        axes = axes.flatten()

        for i, attr in enumerate(attributes):
            ax = axes[i]
            x_labels = []
            y_values = []

            for key, stats in data.items():
                if attr in stats:
                    x_labels.append(key)
                    y_values.append(stats[attr])

            x_pos = np.arange(len(x_labels))
            min_val = min(y_values)
            max_val = max(y_values)
            
            ax.bar(x_pos, y_values, color='steelblue')
            ax.set_title(attr)
            ax.set_xlabel(x_label)
            ax.set_ylabel(attr)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_labels, rotation=45, ha='right')
            ax.set_ylim(min_val * 0.9, max_val * 1.1)  # 动态调整 Y 轴范围

        plt.tight_layout()
        plt.suptitle(title, fontsize=16, y=1.02)
        plt.savefig(save_path)  # 保存图片
        plt.close()

    def plot_averages_by_culture_gender(data, attributes, save_path):
        """绘制 averages_by_culture_gender 的子图"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # 2x3 网格
        axes = axes.flatten()

        for i, attr in enumerate(attributes):
            ax = axes[i]
            x_labels = []
            y_values = []

            for culture, genders in data.items():
                for gender, stats in genders.items():
                    if attr in stats:
                        label = f'{culture}-{gender}'
                        x_labels.append(label)
                        y_values.append(stats[attr])
            
            x_pos = np.arange(len(x_labels))
            min_val = min(y_values)
            max_val = max(y_values)
            
            ax.bar(x_pos, y_values, color='steelblue')
            ax.set_title(attr)
            ax.set_xlabel('Culture-Gender')
            ax.set_ylabel(attr)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_labels, rotation=45, ha='right')
            ax.set_ylim(min_val * 0.9, max_val * 1.1)  # 动态调整 Y 轴范围

        plt.tight_layout()
        plt.suptitle('Averages by Culture-Gender', fontsize=16, y=1.02)
        plt.savefig(save_path)  # 保存图片
        plt.close()

    def plot_top_words_subplot(ax, words, title):
        """在给定的轴上绘制 top_positive_words 或 top_negative_words 的子图"""
        if words:
            labels, scores = zip(*words)  # 解压为两个列表
            x_pos = np.arange(len(labels))
            ax.bar(x_pos, scores, color='steelblue')
            ax.set_title(title)
            ax.set_xlabel('Words')
            ax.set_ylabel('Score')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(labels, rotation=45, ha='right')

    # 计算子图的总数
    total_plots = 0
    for section_name, section_data in sections.items():
        if section_name == 'averages_by_culture_gender':
            for culture, genders in section_data.items():
                total_plots += len(genders) * 2  # 每个性别有正、负词两个图
        else:
            total_plots += len(section_data) * 2  # 每个key有正、负词两个图

    # 创建子图
    fig, axes = plt.subplots(nrows=(total_plots + 1) // 2, ncols=2, figsize=(15, total_plots * 3))
    axes = axes.flatten()  # 将axes展平为一维数组

    plot_index = 0
    for section_name, section_data in sections.items():
        if section_name == 'averages_by_culture_gender':
            for culture, genders in section_data.items():
                for gender, stats in genders.items():
                    plot_top_words_subplot(axes[plot_index], stats.get('top_positive_words', []), f'Top Positive Words in {section_name} - {culture}-{gender}')
                    plot_index += 1
                    plot_top_words_subplot(axes[plot_index], stats.get('top_negative_words', []), f'Top Negative Words in {section_name} - {culture}-{gender}')
                    plot_index += 1
        else:
            for key, stats in section_data.items():
                plot_top_words_subplot(axes[plot_index], stats.get('top_positive_words', []), f'Top Positive Words in {section_name} - {key}')
                plot_index += 1
                plot_top_words_subplot(axes[plot_index], stats.get('top_negative_words', []), f'Top Negative Words in {section_name} - {key}')
                plot_index += 1

    # 调整布局
    plt.tight_layout()
    plt.savefig(f'{output_dir}/combined_top_words.png')  # 保存整合的图表
    plt.show()

    # 绘制三个主要的图
    plot_averages_by_culture_gender(sections['averages_by_culture_gender'], attributes, f'{output_dir}/averages_by_culture_gender.png')
    plot_averages(sections['averages_by_culture'], attributes, 'Culture', 'Averages by Culture', f'{output_dir}/averages_by_culture.png')
    plot_averages(sections['averages_by_gender'], attributes, 'Gender', 'Averages by Gender', f'{output_dir}/averages_by_gender.png')

# 示例调用
# generate_plots('./analysis_results.json', ['normalized_ttr', 'mtld_score', 'polarity', 'subjectivity', 'positive_ratio', 'negative_ratio'], './output')
