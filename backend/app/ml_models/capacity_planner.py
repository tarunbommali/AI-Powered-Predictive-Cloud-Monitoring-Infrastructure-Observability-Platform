"""
Capacity Planning and Auto-Scaling Recommendations
"""
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CapacityPlanner:
    """Capacity planning and scaling recommendations"""
    
    def __init__(self):
        self.thresholds = {
            'cpu_scale_up': 75,
            'memory_scale_up': 80,
            'cpu_scale_down': 30,
            'memory_scale_down': 40
        }
    
    def analyze_capacity(self, historical_metrics, forecast_days=14):
        """Analyze capacity and predict future needs"""
        
        if not historical_metrics or len(historical_metrics) < 7:
            return {'error': 'Insufficient data for capacity planning'}
        
        # Calculate trends
        cpu_values = [m.get('cpu_usage', 0) for m in historical_metrics]
        memory_values = [m.get('memory_usage', 0) for m in historical_metrics]
        
        cpu_trend = self._calculate_trend(cpu_values)
        memory_trend = self._calculate_trend(memory_values)
        
        # Project future usage
        days_data = len(historical_metrics) / 1440  # Assuming 1-minute intervals
        cpu_projection = np.mean(cpu_values) + (cpu_trend * forecast_days)
        memory_projection = np.mean(memory_values) + (memory_trend * forecast_days)
        
        # Determine if scaling needed
        needs_scaling = False
        scale_recommendation = []
        
        if cpu_projection > 85:
            needs_scaling = True
            scale_recommendation.append({
                'metric': 'CPU',
                'current_avg': round(np.mean(cpu_values), 2),
                'projected': round(cpu_projection, 2),
                'action': 'Upgrade to larger instance type',
                'urgency': 'high' if cpu_projection > 95 else 'medium',
                'estimated_days': self._days_until_threshold(cpu_values, cpu_trend, 85)
            })
        
        if memory_projection > 85:
            needs_scaling = True
            scale_recommendation.append({
                'metric': 'Memory',
                'current_avg': round(np.mean(memory_values), 2),
                'projected': round(memory_projection, 2),
                'action': 'Add more RAM or scale horizontally',
                'urgency': 'high' if memory_projection > 95 else 'medium',
                'estimated_days': self._days_until_threshold(memory_values, memory_trend, 85)
            })
        
        return {
            'needs_scaling': needs_scaling,
            'recommendations': scale_recommendation,
            'cpu_trend': round(cpu_trend, 4),
            'memory_trend': round(memory_trend, 4),
            'forecast_period_days': forecast_days,
            'analysis_date': datetime.now().isoformat()
        }
    
    def get_autoscaling_recommendation(self, current_metrics):
        """Get immediate auto-scaling recommendation"""
        
        cpu = current_metrics.get('cpu_usage', 0)
        memory = current_metrics.get('memory_usage', 0)
        
        recommendations = []
        
        # Scale up recommendations
        if cpu > self.thresholds['cpu_scale_up'] or memory > self.thresholds['memory_scale_up']:
            recommendations.append({
                'action': 'scale_up',
                'reason': f"CPU: {cpu}%, Memory: {memory}%",
                'urgency': 'immediate' if cpu > 90 or memory > 90 else 'soon',
                'suggested_instances': self._calculate_instances_needed(cpu, memory),
                'estimated_time': '5 minutes'
            })
        
        # Scale down recommendations
        elif cpu < self.thresholds['cpu_scale_down'] and memory < self.thresholds['memory_scale_down']:
            recommendations.append({
                'action': 'scale_down',
                'reason': f"CPU: {cpu}%, Memory: {memory}% - Underutilized",
                'urgency': 'consider',
                'cost_saving': 'Estimated 30-50% cost reduction',
                'estimated_time': '10 minutes'
            })
        
        return {
            'recommendations': recommendations,
            'current_state': 'optimal' if not recommendations else 'needs_action',
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_trend(self, values):
        """Calculate linear trend"""
        if len(values) < 2:
            return 0
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        return coeffs[0]
    
    def _days_until_threshold(self, values, trend, threshold):
        """Calculate days until threshold is reached"""
        if trend <= 0:
            return None
        current_avg = np.mean(values)
        days = (threshold - current_avg) / trend
        return max(0, round(days, 1))
    
    def _calculate_instances_needed(self, cpu, memory):
        """Calculate how many instances needed"""
        max_util = max(cpu, memory)
        if max_util > 95:
            return 2
        elif max_util > 85:
            return 1
        return 0


capacity_planner = CapacityPlanner()
