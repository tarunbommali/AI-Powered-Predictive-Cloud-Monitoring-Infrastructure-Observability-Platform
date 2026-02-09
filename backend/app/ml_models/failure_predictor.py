"""
System Failure Prediction
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FailurePredictor:
    """Predict potential system failures"""
    
    def __init__(self, model_dir='ml_data/models'):
        self.model_dir = model_dir
        self.model = None
        os.makedirs(model_dir, exist_ok=True)
    
    def prepare_features(self, metrics):
        """Prepare features for prediction"""
        return np.array([[
            metrics.get('cpu_usage', 0),
            metrics.get('memory_usage', 0),
            metrics.get('disk_usage', 0),
            metrics.get('load_1min', 0),
            metrics.get('load_5min', 0),
            metrics.get('network_rx_errors', 0) + metrics.get('network_tx_errors', 0)
        ]])
    
    def predict_failure(self, current_metrics, recent_metrics=None):
        """Predict failure probability"""
        
        # Rule-based prediction (when ML model not available)
        cpu = current_metrics.get('cpu_usage', 0)
        memory = current_metrics.get('memory_usage', 0)
        disk = current_metrics.get('disk_usage', 0)
        load = current_metrics.get('load_1min', 0)
        
        # Calculate risk factors
        risk_score = 0
        risk_factors = []
        
        if cpu > 95:
            risk_score += 30
            risk_factors.append('Critical CPU usage')
        elif cpu > 85:
            risk_score += 15
            risk_factors.append('High CPU usage')
        
        if memory > 95:
            risk_score += 30
            risk_factors.append('Critical memory usage')
        elif memory > 85:
            risk_score += 15
            risk_factors.append('High memory usage')
        
        if disk > 95:
            risk_score += 20
            risk_factors.append('Critical disk usage')
        
        if load > 10:
            risk_score += 20
            risk_factors.append('High system load')
        
        # Check trends if recent metrics available
        if recent_metrics and len(recent_metrics) >= 3:
            cpu_trend = self._calculate_trend([m.get('cpu_usage', 0) for m in recent_metrics])
            if cpu_trend > 5:
                risk_score += 10
                risk_factors.append('Rapidly increasing CPU')
        
        # Calculate failure probability
        failure_probability = min(100, risk_score)
        
        # Determine severity
        if failure_probability >= 70:
            severity = 'critical'
            time_to_failure = '5-30 minutes'
        elif failure_probability >= 40:
            severity = 'warning'
            time_to_failure = '30-60 minutes'
        else:
            severity = 'normal'
            time_to_failure = 'No immediate risk'
        
        return {
            'failure_probability': failure_probability,
            'severity': severity,
            'risk_factors': risk_factors,
            'estimated_time_to_failure': time_to_failure,
            'recommendation': self._get_recommendation(failure_probability, risk_factors),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_trend(self, values):
        """Calculate trend slope"""
        if len(values) < 2:
            return 0
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        return coeffs[0]
    
    def _get_recommendation(self, probability, risk_factors):
        """Get recommendation based on failure probability"""
        if probability >= 70:
            return 'URGENT: Scale up resources immediately or restart services'
        elif probability >= 40:
            return 'WARNING: Monitor closely and prepare for scaling'
        else:
            return 'System operating normally'


failure_predictor = FailurePredictor()
