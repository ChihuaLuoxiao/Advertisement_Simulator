import numpy as np

def dynamic_bid_policy(state, viewer_type):
    """动态投标策略"""
    total_queue = sum(state)
    base_bid = 0.5
    queue_factor = 0.1
    campaign = np.argmax(state)
    bid = base_bid + queue_factor * total_queue
    return bid, campaign

def heuristic_policy(params):
    """启发式策略函数"""
    fixed_bid = np.mean([np.mean(campaign_r) * 0.6 for campaign_r in params['r']])
    alloc_count = np.zeros(params['num_viewer_types'], dtype=int)
    
    def policy(state, viewer_type):
        alloc_count[viewer_type] += 1
        campaign = alloc_count[viewer_type] % params['num_campaigns']
        return fixed_bid, campaign
    
    return policy

def fixed_bid_policy(params):
    """固定投标策略函数"""
    avg_revenue = np.mean([r for campaign in params['r'] for r in campaign])
    optimal_bid = avg_revenue * 0.6
    return lambda s, j: (optimal_bid, 0)