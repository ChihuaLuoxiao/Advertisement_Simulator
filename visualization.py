import matplotlib.pyplot as plt
from config import setup_visualization

def plot_policy_comparison(results, filename="policy_comparison.png"):
    """绘制策略比较结果"""
    setup_visualization()
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values(), color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.ylabel("总利润 ($)")
    plt.title("广告竞价策略性能比较")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

def plot_bid_curve(queue_lengths, optimal_bids, filename="simulated_bid_curve.png"):
    """绘制投标曲线"""
    setup_visualization()
    plt.figure(figsize=(10, 6))
    plt.plot(queue_lengths, optimal_bids, 'o-', linewidth=2)
    plt.xlabel("队列长度 (a)")
    plt.ylabel("最优投标价")
    plt.title("模拟的最优投标策略")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()