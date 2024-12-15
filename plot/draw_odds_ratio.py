import json
import matplotlib.pyplot as plt
import math
from metrics.cal_odds_ratio import traits_data

def plot_odds_ratios(input_file='odds_ratio_results.json', output_file='odds_ratios_plot.png'):
    # 定义一个函数来获取单词的类别
    def get_word_category(word):
        for scale, categories in traits_data.items():
            for category, words in categories.items():
                if word.lower() in words:
                    return category
        return None

    # 定义颜色映射
    color_map = {
        'Powerful': 'green',
        'Powerless': 'red',
        'High status': 'green',
        'Low status': 'red',
        'Dominant': 'green',
        'Dominated': 'red',
        'Wealthy': 'green',
        'Poor': 'red',
        'Confident': 'green',
        'Unconfident': 'red',
        'Competitive': 'green',
        'Unassertive': 'red',
        'Modern': 'green',
        'Traditional': 'red',
        'Science-oriented': 'green',
        'Religious': 'red',
        'Alternative': 'green',
        'Conventional': 'red',
        'Liberal': 'green',
        'Conservative': 'red',
        'Trustworthy': 'green',
        'Untrustworthy': 'red',
        'Sincere': 'green',
        'Dishonest': 'red',
        'Warm': 'green',
        'Cold': 'red',
        'Benevolent': 'green',
        'Threatening': 'red',
        'Likable': 'green',
        'Repellent': 'red',
        'Altruistic': 'green',
        'Egotistic': 'red'
    }

    # 读取JSON数据
    with open(input_file, 'r') as file:
        data = json.load(file)

    # 确定每行的子图数量
    num_columns = 2
    num_data_points = len(data)
    num_rows = math.ceil(num_data_points / num_columns)

    # 创建图形和子图
    fig, axes = plt.subplots(num_rows, num_columns, figsize=(55, 5 * num_rows))

    # 将axes转换为1D数组以便于索引
    axes = axes.flatten()

    # 遍历每条数据
    for i, (key, odds) in enumerate(data.items()):
        # 合并top_odds和bottom_odds
        combined_odds = {**odds['top_odds'], **odds['bottom_odds']}

        # 准备绘图数据
        labels = list(combined_odds.keys())
        values = list(combined_odds.values())

        # 获取每个标签的类别
        categories = [get_word_category(label) for label in labels]
        colors = [color_map.get(category, 'blue') for category in categories]  # 默认颜色为蓝色

        # 创建条形图
        axes[i].bar(labels, values, color=colors)
        axes[i].set_title(key, fontsize=30)
        axes[i].set_ylabel('Odds')
        axes[i].set_xlabel('Labels')
        axes[i].tick_params(axis='x', rotation=45, labelsize=30)

        # 添加水平线在 y=1.0
        axes[i].axhline(y=1.0, color='r', linestyle='--', linewidth=1)

    # 隐藏未使用的子图
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # 调整布局
    plt.tight_layout()

    # 保存图像到指定路径
    plt.savefig(output_file)

    # 显示图像
    plt.show()

# Example usage:
# plot_odds_ratios('odds_ratio_results.json', 'odds_ratios_plot.png')
