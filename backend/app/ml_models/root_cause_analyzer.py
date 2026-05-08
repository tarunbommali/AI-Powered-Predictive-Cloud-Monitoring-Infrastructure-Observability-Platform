# """
# Root Cause Analysis using ML
# """
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)


# class RootCauseAnalyzer:
#     """Analyze root causes of issues"""
    
#     def __init__(self):
#         self.rules = self._initialize_rules()
    
#     def _initialize_rules(self):
#         """Initialize diagnostic rules"""
#         return [
#             {
#                 'name': 'DDoS Attack',
#                 'conditions': lambda m: m.get('network_rx_bytes', 0) > 1000000000 and m.get('cpu_usage', 0) > 80,
#                 'confidence': 0.8,
#                 'recommendation': 'Enable DDoS protection, rate limiting'
#             },
#             {
#                 'name': 'Memory Leak',
#                 'conditions': lambda m: m.get('memory_usage', 0) > 85 and m.get('cpu_usage', 0) < 50,
#                 'confidence': 0.7,
#                 'recommendation': 'Investigate application memory usage, restart services'
#             },
#             {
#                 'name': 'CPU Intensive Process',
#                 'conditions': lambda m: m.get('cpu_usage', 0) > 90 and m.get('load_1min', 0) > 8,
#                 'confidence': 0.9,
#                 'recommendation': 'Identify and optimize CPU-intensive processes'
#             },
#             {
#                 'name': 'Disk I/O Bottleneck',
#                 'conditions': lambda m: m.get('disk_write_bytes', 0) > 100000000 and m.get('load_5min', 0) > 5,
#                 'confidence': 0.75,
#                 'recommendation': 'Optimize disk operations, consider SSD upgrade'
#             },
#             {
#                 'name': 'Network Congestion',
#                 'conditions': lambda m: (m.get('network_rx_errors', 0) + m.get('network_tx_errors', 0)) > 100,
#                 'confidence': 0.7,
#                 'recommendation': 'Check network configuration and bandwidth'
#             }
#         ]
    
#     def analyze(self, metrics, alerts=None):
#         """Analyze metrics and identify root causes"""
        
#         identified_causes = []
        
#         # Check each rule
#         for rule in self.rules:
#             try:
#                 if rule['conditions'](metrics):
#                     identified_causes.append({
#                         'cause': rule['name'],
#                         'confidence': rule['confidence'],
#                         'recommendation': rule['recommendation']
#                     })
#             except:
#                 continue
        
#         # Sort by confidence
#         identified_causes.sort(key=lambda x: x['confidence'], reverse=True)
        
#         # Generate summary
#         if not identified_causes:
#             summary = 'No specific root cause identified. System metrics within normal range.'
#             primary_cause = None
#         else:
#             primary_cause = identified_causes[0]
#             summary = f"Most likely cause: {primary_cause['cause']} (confidence: {primary_cause['confidence']*100:.0f}%)"
        
#         return {
#             'identified_causes': identified_causes,
#             'primary_cause': primary_cause,
#             'summary': summary,
#             'timestamp': datetime.now().isoformat()
#         }


# root_cause_analyzer = RootCauseAnalyzer()






"""
Advanced Root Cause Analysis Engine
AI + Rule-Based Infrastructure Diagnostics
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RootCauseAnalyzer:

    def __init__(self):

        self.rules = self.initialize_rules()

    def initialize_rules(self):

        return [

            {
                'name': 'DDoS Attack',
                'severity': 'critical',
                'confidence': 0.90,
                'condition': lambda m:
                    m.get('network_rx_bytes', 0) > 1_000_000_000
                    and m.get('cpu_usage', 0) > 85,

                'recommendation': (
                    'Enable WAF, rate limiting, '
                    'traffic filtering, and DDoS protection'
                )
            },

            {
                'name': 'Memory Leak',
                'severity': 'high',
                'confidence': 0.85,
                'condition': lambda m:
                    m.get('memory_usage', 0) > 90
                    and m.get('cpu_usage', 0) < 50,

                'recommendation': (
                    'Investigate application memory allocation '
                    'and restart affected services'
                )
            },

            {
                'name': 'CPU Bottleneck',
                'severity': 'critical',
                'confidence': 0.92,
                'condition': lambda m:
                    m.get('cpu_usage', 0) > 92
                    and m.get('load_1min', 0) > 8,

                'recommendation': (
                    'Optimize high CPU processes '
                    'or scale compute resources'
                )
            },

            {
                'name': 'Disk I/O Saturation',
                'severity': 'high',
                'confidence': 0.80,
                'condition': lambda m:
                    m.get('disk_usage', 0) > 90
                    or m.get('disk_write_bytes', 0) > 100_000_000,

                'recommendation': (
                    'Upgrade storage performance '
                    'or clean unnecessary files'
                )
            },

            {
                'name': 'Network Congestion',
                'severity': 'medium',
                'confidence': 0.75,
                'condition': lambda m:
                    (
                        m.get('network_rx_errors', 0)
                        + m.get('network_tx_errors', 0)
                    ) > 100,

                'recommendation': (
                    'Inspect bandwidth, packet loss, '
                    'and network interface configuration'
                )
            },

            {
                'name': 'Infrastructure Overload',
                'severity': 'critical',
                'confidence': 0.88,
                'condition': lambda m:
                    (
                        m.get('cpu_usage', 0)
                        + m.get('memory_usage', 0)
                        + m.get('disk_usage', 0)
                    ) / 3 > 85,

                'recommendation': (
                    'Scale infrastructure immediately '
                    'or distribute workloads'
                )
            },

            {
                'name': 'Application Instability',
                'severity': 'high',
                'confidence': 0.78,
                'condition': lambda m:
                    m.get('load_5min', 0) > 6
                    and m.get('memory_usage', 0) > 75,

                'recommendation': (
                    'Investigate unstable applications '
                    'or memory-intensive services'
                )
            }
        ]

    def analyze(
        self,
        metrics,
        anomaly_result=None,
        failure_prediction=None
    ):

        try:

            identified_causes = []

            for rule in self.rules:

                try:

                    if rule['condition'](metrics):

                        identified_causes.append({
                            'cause': rule['name'],
                            'severity': rule['severity'],
                            'confidence': rule['confidence'],
                            'recommendation': (
                                rule['recommendation']
                            )
                        })

                except Exception:
                    continue

            # Add anomaly context
            if (
                anomaly_result
                and anomaly_result.get('is_anomaly')
            ):

                identified_causes.append({
                    'cause': 'ML Detected Behavioral Anomaly',
                    'severity': anomaly_result.get(
                        'severity',
                        'warning'
                    ),
                    'confidence': anomaly_result.get(
                        'confidence',
                        0.75
                    ),
                    'recommendation': (
                        'Investigate unusual '
                        'system behavior patterns'
                    )
                })

            # Add failure prediction context
            if failure_prediction:

                probability = failure_prediction.get(
                    'failure_probability',
                    0
                )

                if probability > 70:

                    identified_causes.append({
                        'cause': 'Predicted Infrastructure Failure',
                        'severity': 'critical',
                        'confidence': probability / 100,
                        'recommendation': (
                            'Immediate intervention required'
                        )
                    })

            identified_causes.sort(
                key=lambda x: x['confidence'],
                reverse=True
            )

            primary_cause = (
                identified_causes[0]
                if identified_causes
                else None
            )

            summary = self.generate_summary(
                primary_cause
            )

            infrastructure_state = self.determine_state(
                identified_causes
            )

            return {
                'status': 'success',
                'infrastructure_state': (
                    infrastructure_state
                ),
                'identified_causes': identified_causes,
                'primary_cause': primary_cause,
                'summary': summary,
                'recommendation_count': (
                    len(identified_causes)
                ),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(
                f"Root cause analysis failed: {e}"
            )

            return {
                'status': 'error',
                'message': str(e)
            }

    def generate_summary(self, primary_cause):

        if not primary_cause:

            return (
                "No critical infrastructure issues detected"
            )

        return (
            f"Primary issue detected: "
            f"{primary_cause['cause']} "
            f"with confidence "
            f"{primary_cause['confidence'] * 100:.1f}%"
        )

    def determine_state(self, causes):

        if not causes:
            return "healthy"

        severities = [
            c['severity']
            for c in causes
        ]

        if 'critical' in severities:
            return "critical"

        if 'high' in severities:
            return "warning"

        return "stable"


root_cause_analyzer = RootCauseAnalyzer()
