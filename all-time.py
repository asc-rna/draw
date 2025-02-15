import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 数据
labels = ['unfiltered_uniq', 'umi_dedup', 'align_to_genome', 'stage_1_time', 'total_time']
case_data = {
    'case1-base': [1707, 531, 429, 3227, 4376],
    'case2-base': [2184, 743, 580, 4287, 4376],
    'case3-base': [2067, 675, 502, 3876, 4376],
    'case1-opt': [47, 238, 463, 1382, 1947],
    'case2-opt': [63, 332, 573, 1858, 1947],
    'case3-opt': [58, 290, 522, 1619, 1947]
}

colors = ['#f0f0f0', '#404040']  # 从浅灰色到深灰色
cmap = LinearSegmentedColormap.from_list("gradient", colors)
grey = cmap(np.linspace(0, 1, 6))


# 设置图形
fig, ax = plt.subplots(figsize=(8, 6))

# 创建x轴位置
x = np.arange(len(labels))

# 每个条形的宽度
width = 0.1

# 定义不同的标记
# markers = ['o', 'x', 's', '/', '|', '\\']  # 确保有6个不同的标记
# markers = ['', '', '', '\\\\\\', 'oooo', '---']

markers = ['', '', '', 'xxx', 'oo', '--']
ax_dic = {}

# 为每一组数据生成簇状条形图
for i, (case, data) in enumerate(case_data.items()):
    ax_dic[case] = ax.bar(x + (i - 2) * width, data, width, label=case, hatch=markers[i],color=grey[i%3], edgecolor='black')


for i in range(len(labels)):
    label = labels[i]
    for j in range(3):
        base_value = case_data[f'case{j+1}-base'][i]
        opt_value = case_data[f'case{j+1}-opt'][i]
        accel_rate = base_value/opt_value
        bar = ax_dic[f'case{j+1}-opt'][i]
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f' {accel_rate:.1f}X', 
        ha='center', va='bottom', fontsize=8, color='black', rotation=90)

# for case in case_data.keys():
#     for i, data in enumerate(case_data[case]):
#         if i>2:
#             accel_rate = case_data[case][i-3]/case_data[case][i]
#             bar = ax_dic[case][i]
#             ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{accel_rate:.1f}X', 
#             ha='center', va='bottom', fontsize=16, color='black')

# 添加标签和标题
ax.set_ylabel('Time (seconds)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# 显示图形
plt.tight_layout()
plt.savefig("all-time.pdf")