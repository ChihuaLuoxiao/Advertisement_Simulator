from simulator import AdvertisingSimulator
from policies import heuristic_policy, fixed_bid_policy
from visualization import plot_policy_comparison,  plot_bid_curve
import numpy as np

def run_experiments(params=None):
    """运行完整实验"""
    print("="*50)
    print("广告竞价模拟系统")
    print("="*50)
    
    simulator = AdvertisingSimulator(params or {
        'num_campaigns': 3,
        'num_viewer_types': 1,
        'T': 8 * 3600,
        'mu': [2.5],
        'lambda': [0.1, 0.2, 0.3],
        's': [[1], [1], [1]],
        'A': [[50], [50], [50]],
        'r': [[2.5], [3.0], [3.5]],
        'c': [[0.4], [0.4], [0.3]],
        'k': [1],
        'seed': 123
    })
    
    # 实验1: 模拟最优投标曲线
    print("\n" + "="*50)
    print("实验1: 模拟最优投标曲线")
    print("="*50)
    r = simulator.params['r'][0][0]
    A = simulator.params['A'][0][0]
    queue_lengths = np.arange(0, A+1, max(1, A//20))
    optimal_bids = []
    
    for a in queue_lengths:
        if a == 0:
            bid = 0
        else:
            base_bid = r * 0.6
            if a < A * 0.7:
                queue_factor = 0.1 * a
            else:
                queue_factor = 0.1 * (A - a)
            bid = base_bid + queue_factor
        optimal_bids.append(bid)
    
    plot_bid_curve(queue_lengths, optimal_bids)
    print("投标曲线生成完成!")
    
    # 实验2: 策略性能比较
    print("\n" + "="*50)
    print("实验2: 策略性能比较")
    print("="*50)
    events = simulator.generate_events()
    
    policies = {
        "动态策略": simulator.simulate_dynamic_policy,
        "启发式策略": lambda e: simulator.evaluate_policy(heuristic_policy(simulator.params), e),
        "固定投标策略": lambda e: simulator.evaluate_policy(fixed_bid_policy(simulator.params), e)
    }
    
    results = {name: policy_fn(events) for name, policy_fn in policies.items()}
    for name, profit in results.items():
        print(f"{name}利润: ${profit:.2f}")
    
    plot_policy_comparison(results)

    print("\n所有实验完成! 结果图表已保存至当前目录")

if __name__ == "__main__":
    run_experiments()