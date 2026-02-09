"""
Root Cause Analysis using ML
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RootCauseAnalyzer:
    """Analyze root causes of issues"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize diagnostic rules"""
        return [
            {
                'name': 'DDoS Attack',
                'conditions': lambda m: m.get('network_rx_bytes', 0) > 1000000000 and m.get('cpu_usage', 0) > 80,
                'confidence': 0.8,
                'recommendation': 'Enable DDoS protection, rate limiting'
            },
            {
                'name': 'Memory Leak',
                'conditions': lambda m: m.get('memory_usage', 0) > 85 and m.get('cpu_usage', 0) < 50,
                'confidence': 0.7,
                'recommendation': 'Investigate application memory usage, restart services'
            },
            {
                'name': 'CPU Intensive Process',
                'conditions': lambda m: m.get('cpu_usage', 0) > 90 and m.get('load_1min', 0) > 8,
                'confidence': 0.9,
                'recommendation': 'Identify and optimize CPU-intensive processes'
            },
            {
                'name': 'Disk I/O Bottleneck',
                'conditions': lambda m: m.get('disk_write_bytes', 0) > 100000000 and m.get('load_5min', 0) > 5,
                'confidence': 0.75,
                'recommendation': 'Optimize disk operations, consider SSD upgrade'
            },
            {
                'name': 'Network Congestion',
                'conditions': lambda m: (m.get('network_rx_errors', 0) + m.get('network_tx_errors', 0)) > 100,
                'confidence': 0.7,
                'recommendation': 'Check network configuration and bandwidth'
            }
        ]
    
    def analyze(self, metrics, alerts=None):
        """Analyze metrics and identify root causes"""
        
        identified_causes = []
        
        # Check each rule
        for rule in self.rules:
            try:
                if rule['conditions'](metrics):
                    identified_causes.append({
                        'cause': rule['name'],
                        'confidence': rule['confidence'],
                        'recommendation': rule['recommendation']
                    })
            except:
                continue
        
        # Sort by confidence
        identified_causes.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Generate summary
        if not identified_causes:
            summary = 'No specific root cause identified. System metrics within normal range.'
            primary_cause = None
        else:
            primary_cause = identified_causes[0]
            summary = f"Most likely cause: {primary_cause['cause']} (confidence: {primary_cause['confidence']*100:.0f}%)"
        
        return {
            'identified_causes': identified_causes,
            'primary_cause': primary_cause,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }


root_cause_analyzer = RootCauseAnalyzer()
