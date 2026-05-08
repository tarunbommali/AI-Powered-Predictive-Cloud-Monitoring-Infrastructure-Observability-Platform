# """
# Capacity Planning and Auto-Scaling Recommendations
# """
# import numpy as np
# from datetime import datetime, timedelta
# import logging

# logger = logging.getLogger(__name__)


# class CapacityPlanner:
#     """Capacity planning and scaling recommendations"""
    
#     def __init__(self):
#         self.thresholds = {
#             'cpu_scale_up': 75,
#             'memory_scale_up': 80,
#             'cpu_scale_down': 30,
#             'memory_scale_down': 40
#         }
    
#     def analyze_capacity(self, historical_metrics, forecast_days=14):
#         """Analyze capacity and predict future needs"""
        
#         if not historical_metrics or len(historical_metrics) < 7:
#             return {'error': 'Insufficient data for capacity planning'}
        
#         # Calculate trends
#         cpu_values = [m.get('cpu_usage', 0) for m in historical_metrics]
#         memory_values = [m.get('memory_usage', 0) for m in historical_metrics]
        
#         cpu_trend = self._calculate_trend(cpu_values)
#         memory_trend = self._calculate_trend(memory_values)
        
#         # Project future usage
#         days_data = len(historical_metrics) / 1440  # Assuming 1-minute intervals
#         cpu_projection = np.mean(cpu_values) + (cpu_trend * forecast_days)
#         memory_projection = np.mean(memory_values) + (memory_trend * forecast_days)
        
#         # Determine if scaling needed
#         needs_scaling = False
#         scale_recommendation = []
        
#         if cpu_projection > 85:
#             needs_scaling = True
#             scale_recommendation.append({
#                 'metric': 'CPU',
#                 'current_avg': round(np.mean(cpu_values), 2),
#                 'projected': round(cpu_projection, 2),
#                 'action': 'Upgrade to larger instance type',
#                 'urgency': 'high' if cpu_projection > 95 else 'medium',
#                 'estimated_days': self._days_until_threshold(cpu_values, cpu_trend, 85)
#             })
        
#         if memory_projection > 85:
#             needs_scaling = True
#             scale_recommendation.append({
#                 'metric': 'Memory',
#                 'current_avg': round(np.mean(memory_values), 2),
#                 'projected': round(memory_projection, 2),
#                 'action': 'Add more RAM or scale horizontally',
#                 'urgency': 'high' if memory_projection > 95 else 'medium',
#                 'estimated_days': self._days_until_threshold(memory_values, memory_trend, 85)
#             })
        
#         return {
#             'needs_scaling': needs_scaling,
#             'recommendations': scale_recommendation,
#             'cpu_trend': round(cpu_trend, 4),
#             'memory_trend': round(memory_trend, 4),
#             'forecast_period_days': forecast_days,
#             'analysis_date': datetime.now().isoformat()
#         }
    
#     def get_autoscaling_recommendation(self, current_metrics):
#         """Get immediate auto-scaling recommendation"""
        
#         cpu = current_metrics.get('cpu_usage', 0)
#         memory = current_metrics.get('memory_usage', 0)
        
#         recommendations = []
        
#         # Scale up recommendations
#         if cpu > self.thresholds['cpu_scale_up'] or memory > self.thresholds['memory_scale_up']:
#             recommendations.append({
#                 'action': 'scale_up',
#                 'reason': f"CPU: {cpu}%, Memory: {memory}%",
#                 'urgency': 'immediate' if cpu > 90 or memory > 90 else 'soon',
#                 'suggested_instances': self._calculate_instances_needed(cpu, memory),
#                 'estimated_time': '5 minutes'
#             })
        
#         # Scale down recommendations
#         elif cpu < self.thresholds['cpu_scale_down'] and memory < self.thresholds['memory_scale_down']:
#             recommendations.append({
#                 'action': 'scale_down',
#                 'reason': f"CPU: {cpu}%, Memory: {memory}% - Underutilized",
#                 'urgency': 'consider',
#                 'cost_saving': 'Estimated 30-50% cost reduction',
#                 'estimated_time': '10 minutes'
#             })
        
#         return {
#             'recommendations': recommendations,
#             'current_state': 'optimal' if not recommendations else 'needs_action',
#             'timestamp': datetime.now().isoformat()
#         }
    
#     def _calculate_trend(self, values):
#         """Calculate linear trend"""
#         if len(values) < 2:
#             return 0
#         x = np.arange(len(values))
#         coeffs = np.polyfit(x, values, 1)
#         return coeffs[0]
    
#     def _days_until_threshold(self, values, trend, threshold):
#         """Calculate days until threshold is reached"""
#         if trend <= 0:
#             return None
#         current_avg = np.mean(values)
#         days = (threshold - current_avg) / trend
#         return max(0, round(days, 1))
    
#     def _calculate_instances_needed(self, cpu, memory):
#         """Calculate how many instances needed"""
#         max_util = max(cpu, memory)
#         if max_util > 95:
#             return 2
#         elif max_util > 85:
#             return 1
#         return 0


# capacity_planner = CapacityPlanner()








"""
Advanced Capacity Planning & AI Auto-Scaling
"""

import numpy as np
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CapacityPlanner:

    def __init__(self):

        self.thresholds = {
            'cpu_scale_up': 80,
            'memory_scale_up': 85,
            'disk_scale_up': 90,
            'cpu_scale_down': 25,
            'memory_scale_down': 35
        }

    def analyze_capacity(
        self,
        historical_metrics,
        forecast_days=7
    ):

        try:

            if len(historical_metrics) < 20:

                return {
                    'status': 'error',
                    'message': 'Need at least 20 samples'
                }

            cpu_values = [
                m.get('cpu_usage', 0)
                for m in historical_metrics
            ]

            memory_values = [
                m.get('memory_usage', 0)
                for m in historical_metrics
            ]

            disk_values = [
                m.get('disk_usage', 0)
                for m in historical_metrics
            ]

            cpu_trend = self.calculate_trend(
                cpu_values
            )

            memory_trend = self.calculate_trend(
                memory_values
            )

            disk_trend = self.calculate_trend(
                disk_values
            )

            cpu_projection = (
                np.mean(cpu_values)
                + (cpu_trend * forecast_days)
            )

            memory_projection = (
                np.mean(memory_values)
                + (memory_trend * forecast_days)
            )

            disk_projection = (
                np.mean(disk_values)
                + (disk_trend * forecast_days)
            )

            scaling_needed = (
                cpu_projection > 85
                or memory_projection > 85
                or disk_projection > 90
            )

            infrastructure_pressure = self.calculate_pressure(
                cpu_projection,
                memory_projection,
                disk_projection
            )

            recommendations = self.generate_recommendations(
                cpu_projection,
                memory_projection,
                disk_projection
            )

            cost_optimization = self.calculate_cost_optimization(
                cpu_values,
                memory_values
            )

            return {
                'status': 'success',
                'scaling_needed': scaling_needed,
                'forecast_days': forecast_days,
                'infrastructure_pressure': infrastructure_pressure,
                'projections': {
                    'cpu_projection': round(cpu_projection, 2),
                    'memory_projection': round(memory_projection, 2),
                    'disk_projection': round(disk_projection, 2)
                },
                'trends': {
                    'cpu_trend': round(cpu_trend, 4),
                    'memory_trend': round(memory_trend, 4),
                    'disk_trend': round(disk_trend, 4)
                },
                'recommendations': recommendations,
                'cost_optimization': cost_optimization,
                'analysis_time': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(f"Capacity analysis failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def get_autoscaling_recommendation(
        self,
        current_metrics,
        cpu_prediction=None,
        memory_prediction=None,
        failure_prediction=None
    ):

        try:

            cpu = current_metrics.get(
                'cpu_usage',
                0
            )

            memory = current_metrics.get(
                'memory_usage',
                0
            )

            disk = current_metrics.get(
                'disk_usage',
                0
            )

            actions = []

            severity = "normal"

            predicted_cpu = cpu

            predicted_memory = memory

            if cpu_prediction:

                predictions = cpu_prediction.get(
                    'predictions',
                    []
                )

                if predictions:
                    predicted_cpu = max([
                        p.get('predicted_cpu', cpu)
                        for p in predictions
                    ])

            if memory_prediction:

                predictions = memory_prediction.get(
                    'predictions',
                    []
                )

                if predictions:
                    predicted_memory = max([
                        p.get(
                            'predicted_memory',
                            memory
                        )
                        for p in predictions
                    ])

            failure_probability = 0

            if failure_prediction:

                failure_probability = (
                    failure_prediction.get(
                        'failure_probability',
                        0
                    )
                )

            # Scale Up Logic
            if (
                predicted_cpu > 85
                or predicted_memory > 85
                or failure_probability > 70
            ):

                severity = "critical"

                actions.append({
                    'action': 'scale_up',
                    'reason': (
                        f'Predicted CPU: {predicted_cpu:.2f}% '
                        f'Predicted Memory: {predicted_memory:.2f}%'
                    ),
                    'recommended_instance': (
                        self.recommend_instance_type(
                            predicted_cpu,
                            predicted_memory
                        )
                    ),
                    'estimated_instances_needed': (
                        self.calculate_instances_needed(
                            predicted_cpu,
                            predicted_memory
                        )
                    ),
                    'urgency': 'immediate'
                })

            # Scale Down Logic
            elif (
                cpu < 30
                and memory < 35
            ):

                severity = "optimization"

                actions.append({
                    'action': 'scale_down',
                    'reason': (
                        'Resources underutilized'
                    ),
                    'estimated_cost_saving': (
                        '30-50%'
                    ),
                    'urgency': 'consider'
                })

            # Stable
            else:

                actions.append({
                    'action': 'maintain',
                    'reason': (
                        'Infrastructure stable'
                    ),
                    'urgency': 'none'
                })

            return {
                'status': 'success',
                'severity': severity,
                'actions': actions,
                'predicted_cpu': round(predicted_cpu, 2),
                'predicted_memory': round(
                    predicted_memory,
                    2
                ),
                'failure_probability': failure_probability,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(f"Autoscaling failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def calculate_trend(self, values):

        if len(values) < 2:
            return 0

        x = np.arange(len(values))

        slope, intercept = np.polyfit(
            x,
            values,
            1
        )

        return slope

    def calculate_pressure(
        self,
        cpu,
        memory,
        disk
    ):

        avg_pressure = (
            cpu + memory + disk
        ) / 3

        if avg_pressure > 90:
            return "critical"

        elif avg_pressure > 75:
            return "high"

        elif avg_pressure > 50:
            return "moderate"

        return "low"

    def generate_recommendations(
        self,
        cpu,
        memory,
        disk
    ):

        recommendations = []

        if cpu > 85:

            recommendations.append(
                "Increase compute resources"
            )

        if memory > 85:

            recommendations.append(
                "Upgrade RAM capacity"
            )

        if disk > 90:

            recommendations.append(
                "Expand storage immediately"
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Infrastructure capacity healthy"
            )

        return recommendations

    def calculate_cost_optimization(
        self,
        cpu_values,
        memory_values
    ):

        avg_cpu = np.mean(cpu_values)

        avg_memory = np.mean(memory_values)

        if avg_cpu < 30 and avg_memory < 40:

            return {
                'optimization_possible': True,
                'recommendation': (
                    'Downsize instance type'
                ),
                'estimated_savings': '30-50%'
            }

        return {
            'optimization_possible': False,
            'recommendation': (
                'Current sizing appropriate'
            )
        }

    def recommend_instance_type(
        self,
        cpu,
        memory
    ):

        pressure = max(cpu, memory)

        if pressure > 95:
            return "c5.2xlarge"

        elif pressure > 85:
            return "c5.xlarge"

        elif pressure > 70:
            return "t3.large"

        return "Current instance sufficient"

    def calculate_instances_needed(
        self,
        cpu,
        memory
    ):

        pressure = max(cpu, memory)

        if pressure > 95:
            return 3

        elif pressure > 85:
            return 2

        elif pressure > 70:
            return 1

        return 0


capacity_planner = CapacityPlanner()
