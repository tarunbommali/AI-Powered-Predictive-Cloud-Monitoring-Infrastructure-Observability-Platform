"""
Infrastructure Rule Engine
"""

from datetime import datetime


class RuleEngine:

    def evaluate(self, metrics):

        alerts = []

        cpu = metrics.get('cpu_usage', 0)

        memory = metrics.get(
            'memory_usage',
            0
        )

        disk = metrics.get(
            'disk_usage',
            0
        )

        load = metrics.get(
            'load_1min',
            0
        )

        if cpu > 90:

            alerts.append({
                'type': 'critical',
                'message': (
                    'Critical CPU usage detected'
                )
            })

        elif cpu > 75:

            alerts.append({
                'type': 'warning',
                'message': (
                    'High CPU usage'
                )
            })

        if memory > 90:

            alerts.append({
                'type': 'critical',
                'message': (
                    'Critical memory usage'
                )
            })

        if disk > 95:

            alerts.append({
                'type': 'critical',
                'message': (
                    'Disk almost full'
                )
            })

        if load > 8:

            alerts.append({
                'type': 'warning',
                'message': (
                    'System load unusually high'
                )
            })

        return {
            'alerts': alerts,
            'healthy': len(alerts) == 0,
            'timestamp': (
                datetime.now().isoformat()
            )
        }


rule_engine = RuleEngine()
