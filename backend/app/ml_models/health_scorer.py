"""
Instance Health Scoring System
"""
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HealthScorer:
    """Calculate health scores for instances"""
    
    def __init__(self):
        self.weights = {
            'cpu': 0.25,
            'memory': 0.25,
            'disk': 0.20,
            'network': 0.10,
            'anomaly': 0.15,
            'stability': 0.05
        }
    
    def calculate_health_score(self, metrics, anomaly_score=None):
        """Calculate overall health score (0-100)"""
        
        # CPU score (inverse - lower is better)
        cpu_score = max(0, 100 - metrics.get('cpu_usage', 0))
        
        # Memory score
        memory_score = max(0, 100 - metrics.get('memory_usage', 0))
        
        # Disk score
        disk_score = max(0, 100 - metrics.get('disk_usage', 0))
        
        # Network score (based on errors)
        network_errors = metrics.get('network_rx_errors', 0) + metrics.get('network_tx_errors', 0)
        network_score = max(0, 100 - (network_errors * 10))
        
        # Anomaly score
        if anomaly_score and anomaly_score.get('is_anomaly'):
            anomaly_penalty = anomaly_score.get('confidence', 0) * 100
            anomaly_component = max(0, 100 - anomaly_penalty)
        else:
            anomaly_component = 100
        
        # Stability score (based on load average)
        load = metrics.get('load_1min', 0)
        cpu_count = metrics.get('cpu_count', 4)
        stability_score = max(0, 100 - (load / cpu_count * 100))
        
        # Weighted average
        health_score = (
            cpu_score * self.weights['cpu'] +
            memory_score * self.weights['memory'] +
            disk_score * self.weights['disk'] +
            network_score * self.weights['network'] +
            anomaly_component * self.weights['anomaly'] +
            stability_score * self.weights['stability']
        )
        
        # Determine status
        if health_score >= 90:
            status = 'excellent'
            color = 'success'
        elif health_score >= 70:
            status = 'good'
            color = 'success'
        elif health_score >= 50:
            status = 'warning'
            color = 'warning'
        else:
            status = 'critical'
            color = 'danger'
        
        return {
            'health_score': round(health_score, 2),
            'status': status,
            'color': color,
            'components': {
                'cpu_score': round(cpu_score, 2),
                'memory_score': round(memory_score, 2),
                'disk_score': round(disk_score, 2),
                'network_score': round(network_score, 2),
                'anomaly_score': round(anomaly_component, 2),
                'stability_score': round(stability_score, 2)
            },
            'timestamp': datetime.now().isoformat()
        }


health_scorer = HealthScorer()
