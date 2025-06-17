# Advertisement_Simulator
文件结构
advertising_simulator/
├── __init__.py
├── config.py          # 配置和常量
├── simulator.py       # 主模拟器类
├── policies.py        # 各种策略实现
├── utils.py           # 工具函数
├── experiments.py     # 实验运行代码
└── visualization.py   # 可视化相关函数
README.md          # 本文件

安装与使用
依赖安装
bash
pip install numpy pandas matplotlib scipy cvxpy tqdm seaborn

快速开始
python
from advertising_simulator import run_experiments

# 使用默认参数运行完整实验
run_experiments()

# 使用自定义参数
custom_params = {
    'num_campaigns': 2,
    'num_viewer_types': 2,
    'T': 8 * 3600,  # 8小时模拟
    'mu': [1.5, 2.0],  # 观众到达率
    'lambda': [0.1, 0.15],  # 活动到达率
    's': [[5, 3], [4, 2]],  # 印象需求
    'A': [[15, 10], [12, 8]],  # 队列容量
    'r': [[1.5, 1.2], [1.8, 1.0]],  # 单位收益
    'c': [[0.05, 0.04], [0.06, 0.03]],  # 单位延迟成本
    'k': [1, 1.2],  # 胜率函数参数
    'seed': 42  # 随机种子
}
run_experiments(custom_params)
主要类与方法
AdvertisingSimulator 类
广告竞价系统模拟器核心类。

主要方法：
generate_events(): 生成模拟事件序列

simulate_dynamic_policy(events): 运行动态策略模拟

evaluate_policy(policy, events, num_runs): 评估指定策略性能

reset_state(): 重置模拟器状态

策略实现
在policies.py中实现了以下策略：

动态投标策略 (dynamic_bid_policy)

基于当前队列长度动态调整投标价

启发式策略 (heuristic_policy)

使用固定投标价和轮询分配

固定投标策略 (fixed_bid_policy)

使用固定投标价

线性投标策略 (linear_bid_policy)

投标价与队列长度线性相关

实验内容
运行run_experiments()将执行以下实验：

投标曲线模拟

模拟不同队列长度下的最优投标价

生成simulated_bid_curve.png

策略性能比较

比较四种策略的总利润

生成policy_comparison.png

敏感性分析

分析延迟成本对利润的影响

生成sensitivity_c_multiplier.png
