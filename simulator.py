import numpy as np
from scipy.stats import expon
from config import DEFAULT_PARAMS
from policies import dynamic_bid_policy

class AdvertisingSimulator:
    """广告竞价系统模拟器"""
    
    def __init__(self, params=None):
        self.params = params or DEFAULT_PARAMS
        np.random.seed(self.params['seed'])
        self.reset_state()
    
    def reset_state(self):
        """重置系统状态"""
        self.state = np.zeros((self.params['num_campaigns'], 
                            self.params['num_viewer_types']))
        self.event_log = []
        self.time = 0
    
    def win_probability(self, bid, viewer_type):
        """投标胜率函数"""
        k = self.params['k'][viewer_type]
        return 1 - np.exp(-k * bid) if bid > 0 else 0
    
    def generate_events(self):
        """生成观众和广告活动到达事件序列"""
        events = []
        
        # 生成观众到达事件
        for j in range(self.params['num_viewer_types']):
            rate = self.params['mu'][j]
            n_events = max(100, int(2 * rate * self.params['T']))
            interarrivals = expon.rvs(scale=1/rate, size=n_events)
            times = np.cumsum(interarrivals)
            times = times[times < self.params['T']]
            
            for t in times:
                events.append({
                    'time': t,
                    'type': 'viewer',
                    'viewer_type': j
                })
        
        # 生成广告活动到达事件
        for i in range(self.params['num_campaigns']):
            rate = self.params['lambda'][i]
            n_events = max(50, int(2 * rate * self.params['T']))
            interarrivals = expon.rvs(scale=1/rate, size=n_events)
            times = np.cumsum(interarrivals)
            times = times[times < self.params['T']]
            
            for t in times:
                events.append({
                    'time': t,
                    'type': 'campaign',
                    'campaign_type': i
                })
        
        events.sort(key=lambda x: x['time'])
        return events
    
    def simulate_dynamic_policy(self, events):
        """模拟动态策略"""
        self.reset_state()
        total_profit = 0
        last_time = 0
        
        for event in events:
            dt = event['time'] - last_time
            last_time = event['time']
            
            # 计算延迟成本
            delay_cost = 0
            for i in range(self.params['num_campaigns']):
                for j in range(self.params['num_viewer_types']):
                    delay_cost += self.params['c'][i][j] * self.state[i, j] * dt
            total_profit -= delay_cost
            
            if event['type'] == 'viewer':
                j = event['viewer_type']
                bid, i_alloc = dynamic_bid_policy(self.state[:, j], j)
                win = np.random.rand() < self.win_probability(bid, j)
                
                if win and self.state[i_alloc, j] > 0:
                    self.state[i_alloc, j] -= 1
                    revenue = self.params['r'][i_alloc][j]
                    total_profit += revenue - bid
                else:
                    revenue = 0
                
                self.event_log.append({
                    'time': event['time'],
                    'type': 'viewer',
                    'viewer_type': j,
                    'bid': bid,
                    'win': win,
                    'revenue': revenue if win else 0,
                    'cost': bid if win else 0,
                    'campaign_alloc': i_alloc
                })
                
            else:  # 广告活动到达
                i = event['campaign_type']
                for j in range(self.params['num_viewer_types']):
                    s_ij = self.params['s'][i][j]
                    accepted = min(s_ij, self.params['A'][i][j] - self.state[i, j])
                    self.state[i, j] += accepted
                
                self.event_log.append({
                    'time': event['time'],
                    'type': 'campaign',
                    'campaign_type': i,
                    'impressions_accepted': sum(self.params['s'][i])
                })
        
        return total_profit
    
    def evaluate_policy(self, policy, events=None, num_runs=1):
        """评估策略性能"""
        if events is None:
            events = self.generate_events()
            
        total_profit = 0
        for _ in range(num_runs):
            self.reset_state()
            last_time = 0
            profit = 0
            
            for event in events:
                dt = event['time'] - last_time
                last_time = event['time']
                
                for i in range(self.params['num_campaigns']):
                    for j in range(self.params['num_viewer_types']):
                        profit -= self.params['c'][i][j] * self.state[i, j] * dt
                
                if event['type'] == 'viewer':
                    j = event['viewer_type']
                    bid, i_alloc = policy(self.state[:, j], j)
                    
                    win = np.random.rand() < self.win_probability(bid, j)
                    if win and self.state[i_alloc, j] > 0:
                        self.state[i_alloc, j] -= 1
                        profit += self.params['r'][i_alloc][j] - bid
                
                else:  
                    i = event['campaign_type']
                    for j in range(self.params['num_viewer_types']):
                        s_ij = self.params['s'][i][j]
                        accepted = min(s_ij, self.params['A'][i][j] - self.state[i, j])
                        self.state[i, j] += accepted
            
            total_profit += profit
        if total_profit / num_runs > 0:
            return total_profit / num_runs
        else:
            return 0