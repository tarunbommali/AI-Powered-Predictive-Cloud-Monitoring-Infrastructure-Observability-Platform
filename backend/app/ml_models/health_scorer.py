# """
# Instance Health Scoring System
# """
# import numpy as np
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)


# class HealthScorer:
#     """Calculate health scores for instances"""
    
#     def __init__(self):
#         self.weights = {
#             'cpu': 0.25,
#             'memory': 0.25,
#             'disk': 0.20,
#             'network': 0.10,
#             'anomaly': 0.15,
#             'stability': 0.05
#         }
    
#     def calculate_health_score(self, metrics, anomaly_score=None):
#         """Calculate overall health score (0-100)"""
        
#         # CPU score (inverse - lower is better)
#         cpu_score = max(0, 100 - metrics.get('cpu_usage', 0))
        
#         # Memory score
#         memory_score = max(0, 100 - metrics.get('memory_usage', 0))
        
#         # Disk score
#         disk_score = max(0, 100 - metrics.get('disk_usage', 0))
        
#         # Network score (based on errors)
#         network_errors = metrics.get('network_rx_errors', 0) + metrics.get('network_tx_errors', 0)
#         network_score = max(0, 100 - (network_errors * 10))
        
#         # Anomaly score
#         if anomaly_score and anomaly_score.get('is_anomaly'):
#             anomaly_penalty = anomaly_score.get('confidence', 0) * 100
#             anomaly_component = max(0, 100 - anomaly_penalty)
#         else:
#             anomaly_component = 100
        
#         # Stability score (based on load average)
#         load = metrics.get('load_1min', 0)
#         cpu_count = metrics.get('cpu_count', 4)
#         stability_score = max(0, 100 - (load / cpu_count * 100))
        
#         # Weighted average
#         health_score = (
#             cpu_score * self.weights['cpu'] +
#             memory_score * self.weights['memory'] +
#             disk_score * self.weights['disk'] +
#             network_score * self.weights['network'] +
#             anomaly_component * self.weights['anomaly'] +
#             stability_score * self.weights['stability']
#         )
        
#         # Determine status
#         if health_score >= 90:
#             status = 'excellent'
#             color = 'success'
#         elif health_score >= 70:
#             status = 'good'
#             color = 'success'
#         elif health_score >= 50:
#             status = 'warning'
#             color = 'warning'
#         else:
#             status = 'critical'
#             color = 'danger'
        
#         return {
#             'health_score': round(health_score, 2),
#             'status': status,
#             'color': color,
#             'components': {
#                 'cpu_score': round(cpu_score, 2),
#                 'memory_score': round(memory_score, 2),
#                 'disk_score': round(disk_score, 2),
#                 'network_score': round(network_score, 2),
#                 'anomaly_score': round(anomaly_component, 2),
#                 'stability_score': round(stability_score, 2)
#             },
#             'timestamp': datetime.now().isoformat()
#         }


# health_scorer = HealthScorer()




"""
Advanced AI Health Scoring System
Hybrid ML + Rule Intelligence
"""

import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HealthScorer:

    def __init__(self):

        self.weights = {
            'cpu': 0.20,
            'memory': 0.20,
            'disk': 0.15,
            'network': 0.10,
            'anomaly': 0.15,
            'failure_risk': 0.15,
            'stability': 0.05
        }

    def calculate_health_score(
        self,
        metrics,
        anomaly_result=None,
        failure_prediction=None
    ):

        try:

            cpu_score = self.calculate_cpu_score(
                metrics.get('cpu_usage', 0)
            )

            memory_score = self.calculate_memory_score(
                metrics.get('memory_usage', 0)
            )

            disk_score = self.calculate_disk_score(
                metrics.get('disk_usage', 0)
            )

            network_score = self.calculate_network_score(
                metrics
            )

            anomaly_score = self.calculate_anomaly_score(
                anomaly_result
            )

            failure_score = self.calculate_failure_score(
                failure_prediction
            )

            stability_score = self.calculate_stability_score(
                metrics
            )

            final_score = (
                cpu_score * self.weights['cpu']
                + memory_score * self.weights['memory']
                + disk_score * self.weights['disk']
                + network_score * self.weights['network']
                + anomaly_score * self.weights['anomaly']
                + failure_score * self.weights['failure_risk']
                + stability_score * self.weights['stability']
            )

            final_score = max(0, min(100, final_score))

            status, color = self.determine_status(
                final_score
            )

            risk_level = self.calculate_risk_level(
                final_score
            )

            recommendations = self.generate_recommendations(
                metrics,
                anomaly_result,
                failure_prediction
            )

            return {
                'health_score': round(final_score, 2),
                'status': status,
                'color': color,
                'risk_level': risk_level,
                'components': {
                    'cpu_score': round(cpu_score, 2),
                    'memory_score': round(memory_score, 2),
                    'disk_score': round(disk_score, 2),
                    'network_score': round(network_score, 2),
                    'anomaly_score': round(anomaly_score, 2),
                    'failure_score': round(failure_score, 2),
                    'stability_score': round(stability_score, 2)
                },
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(f"Health score failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def calculate_cpu_score(self, cpu):

        if cpu >= 95:
            return 5

        elif cpu >= 85:
            return 25

        elif cpu >= 70:
            return 50

        elif cpu >= 50:
            return 75

        return 100

    def calculate_memory_score(self, memory):

        if memory >= 95:
            return 5

        elif memory >= 85:
            return 25

        elif memory >= 70:
            return 50

        elif memory >= 50:
            return 75

        return 100

    def calculate_disk_score(self, disk):

        if disk >= 98:
            return 0

        elif disk >= 90:
            return 20

        elif disk >= 80:
            return 50

        elif disk >= 60:
            return 75

        return 100

    def calculate_network_score(self, metrics):

        rx_errors = metrics.get(
            'network_rx_errors',
            0
        )

        tx_errors = metrics.get(
            'network_tx_errors',
            0
        )

        total_errors = rx_errors + tx_errors

        if total_errors > 100:
            return 20

        elif total_errors > 50:
            return 50

        elif total_errors > 10:
            return 75

        return 100

    def calculate_anomaly_score(
        self,
        anomaly_result
    ):

        if not anomaly_result:
            return 100

        if not anomaly_result.get('is_anomaly'):
            return 100

        confidence = anomaly_result.get(
            'confidence',
            0
        )

        return max(0, 100 - (confidence * 100))

    def calculate_failure_score(
        self,
        failure_prediction
    ):

        if not failure_prediction:
            return 100

        failure_probability = failure_prediction.get(
            'failure_probability',
            0
        )

        return max(0, 100 - failure_probability)

    def calculate_stability_score(self, metrics):

        load1 = metrics.get('load_1min', 0)

        load5 = metrics.get('load_5min', 0)

        load15 = metrics.get('load_15min', 0)

        avg_load = (
            load1 + load5 + load15
        ) / 3

        cpu_count = metrics.get('cpu_count', 4)

        normalized_load = avg_load / cpu_count

        stability = max(
            0,
            100 - (normalized_load * 100)
        )

        return stability

    def determine_status(self, score):

        if score >= 90:
            return "excellent", "success"

        elif score >= 75:
            return "good", "success"

        elif score >= 55:
            return "warning", "warning"

        elif score >= 35:
            return "critical", "danger"

        return "failure_risk", "danger"

    def calculate_risk_level(self, score):

        if score >= 85:
            return "low"

        elif score >= 60:
            return "medium"

        elif score >= 40:
            return "high"

        return "critical"

    def generate_recommendations(
        self,
        metrics,
        anomaly_result,
        failure_prediction
    ):

        recommendations = []

        cpu = metrics.get('cpu_usage', 0)

        memory = metrics.get('memory_usage', 0)

        disk = metrics.get('disk_usage', 0)

        if cpu > 85:
            recommendations.append(
                "Scale CPU resources or optimize workloads"
            )

        if memory > 85:
            recommendations.append(
                "Increase memory allocation"
            )

        if disk > 90:
            recommendations.append(
                "Clean disk space immediately"
            )

        if anomaly_result and anomaly_result.get(
            'is_anomaly'
        ):
            recommendations.append(
                "Investigate abnormal system behavior"
            )

        if failure_prediction:

            probability = failure_prediction.get(
                'failure_probability',
                0
            )

            if probability > 70:
                recommendations.append(
                    "URGENT: Immediate scaling recommended"
                )

            elif probability > 40:
                recommendations.append(
                    "Monitor closely for possible instability"
                )

        if len(recommendations) == 0:

            recommendations.append(
                "System operating optimally"
            )

        return recommendations


health_scorer = HealthScorer()

