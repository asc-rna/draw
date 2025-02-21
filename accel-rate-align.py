import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


# 优化后的运行时间（秒）
times = [499, 287, 374, 1802, 471, 269, 282, 206]
text = [f">900" if x > 90000 else f"{x}" for x in times]
times = [900 if x > 900 else x for x in times]

# 假设原始运行时间（8min50s = 530秒）
# original_time = 501

# 计算加速比
# speedup = [original_time / time for time in times]

# 设置X轴位置
x = [1,1.41, 3,3.41, 5,5.41, 7,7.41]
# print(x)

# 重新绘制图表：只包含条形图，修改图例位置，修改X轴标签
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图：显示优化后的运行时间
# bars = ax.bar(x, times, width=0.4, color='white', edgecolor='black', hatch='/')

hatch_patterns = ['/', '/', '+', '+', '/', '/', '+', '+']

# for i, bar in enumerate(bars):
for i, time in enumerate(times):
    bar = ax.bar(x[i], times[i], width=0.4, color='white', edgecolor='black', hatch=hatch_patterns[i]*3)
    ax.text(bar[0].get_x() + bar[0].get_width() / 2, bar[0].get_height(), f'{text[i]}', 
            ha='center', va='bottom', fontsize=16, color='black')

# 手动创建legend patches对应hatch模式
legends = ['align_to_genome', 'align_to_ncrna']
legend_patches = [mpatches.Patch(facecolor='white', edgecolor='black', hatch=hatch*3, label=f'{legends[i]}') for i, hatch in enumerate(hatch_patterns[1:3])]

# 添加图例
ax.legend(handles=legend_patches)


# 设置X轴标签
ax.set_xticks(x)
ax.set_xticklabels(['p16', 'p32', 'p16', 'p26', 'opt\np16', 'opt\np32', 'opt\np16', 'opt\np26'], fontsize=14)

# 设置Y轴标签
ax.set_ylabel("Elapsed Time / s ", fontsize=14, color='black')
ax.tick_params(axis='y', labelcolor='black')

# # 添加标题
# plt.title("Execution Time for Different Optimization Iterations", fontsize=16)

# # 调整图例位置避免遮住标题
# fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.8, 1))

# 显示图表
plt.tight_layout()
plt.savefig("accel-rate-align.pdf")
