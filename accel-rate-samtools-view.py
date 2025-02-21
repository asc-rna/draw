import matplotlib.pyplot as plt
import numpy as np

# 优化后的运行时间（秒）
times = [61.71, 37.01, 22.30, 23.51, 23.03]

# 假设原始运行时间（8min50s = 530秒）
original_time = times[0]

# 计算加速比
speedup = [original_time / time for time in times]

# 设置X轴位置
x = np.arange(1, len(times) + 1)

# 重新绘制图表：只包含条形图，修改图例位置，修改X轴标签
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图：显示优化后的运行时间
bars = ax.bar(x, times, width=0.4, color='white', edgecolor='black', hatch='/')
# 绘制折线图：时间
# bars = ax.plot(x, times, marker='o', color='black')

for i, bar in enumerate(bars):
    #ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{times[i]:.1f}s', ha='center', va='bottom', fontsize=16, color='black')
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{speedup[i]:.1f}X' if i > 0 else '', ha='center', va='bottom', fontsize=16, color='black')


# 设置X轴标签
ax.set_xticks(x)
ax.set_xticklabels(['single thread', '-@ 1', '-@ 2', '-@ 3', '-@ 4'], fontsize=12)

# 设置Y轴标签
ax.set_ylabel("Elapsed Time / s ", fontsize=14, color='black')
ax.tick_params(axis='y', labelcolor='black')

# # 添加标题
# plt.title("Execution Time for Different Optimization Iterations", fontsize=16)

# # 调整图例位置避免遮住标题
# fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.8, 1))

# 显示图表
plt.tight_layout()
plt.savefig("accel-rate-samtools-view.pdf")
