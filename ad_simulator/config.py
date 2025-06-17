# 广告模拟系统的默认配置和常量
import numpy as np

DEFAULT_PARAMS = {
    'num_campaigns': 1,
    'num_viewer_types': 1,
    'T': 24 * 3600,
    'mu': [0.5],
    'lambda': [0.2],
    's': [[5, 3]],
    'A': [[15, 10]],
    'r': [[1.5, 1.2]],
    'c': [[0.05, 0.04]],
    'k': [1],
    'seed': 1
}

# 可视化设置
def setup_visualization():
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题