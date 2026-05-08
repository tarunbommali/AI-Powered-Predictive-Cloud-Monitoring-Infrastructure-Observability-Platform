
"""
Advanced System Failure Prediction
Hybrid ML + Rule-Based Intelligence
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FailurePredictor:

    def __init__(self, model_dir='ml_data/models'):

        self.model_dir = model_dir

        os.makedirs(model_dir, exist_ok=True)

        self.scaler = StandardScaler()

        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42
        )

        self.is_trained = False

    def prepare_features(self, metrics_data):

        features = []

        labels = []

        for metric in metrics_data:

            cpu = metric.get('cpu_usage', 0)

            memory = metric.get('memory_usage', 0)

            disk = metric.get('disk_usage', 0)

            load1 = metric.get('load_1min', 0)

            load5 = metric.get('load_5min', 0)

            network_errors = (
                metric.get('network_rx_errors', 0)
                + metric.get('network_tx_errors', 0)
            )

            cpu_memory_ratio = cpu / (memory + 1)

            system_pressure = (
                cpu + memory + disk
            ) / 3

            feature_vector = [
                cpu,
                memory,
                disk,
                load1,
                load5,
                network_errors,
                cpu_memory_ratio,
                system_pressure
            ]

            features.append(feature_vector)

            # Synthetic failure label generation
            failure = 0

            if (
                cpu > 92
                or memory > 95
                or disk > 97
                or load1 > 8
                or network_errors > 100
            ):
                failure = 1

            labels.append(failure)

        return np.array(features), np.array(labels)

    def train(self, historical_data):

        logger.info("Training failure prediction model...")

        try:

            X, y = self.prepare_features(historical_data)

            if len(X) < 20:

                return {
                    'status': 'error',
                    'message': 'Need minimum 20 samples'
                }

            X_scaled = self.scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled,
                y,
                test_size=0.2,
                random_state=42
            )

            self.model.fit(X_train, y_train)

            predictions = self.model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)

            self.is_trained = True

            self.save_model()

            return {
                'status': 'success',
                'samples_trained': len(X),
                'accuracy': round(float(accuracy), 3)
            }

        except Exception as e:

            logger.error(f"Failure predictor training failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def predict_failure(self, current_metrics, recent_metrics=None):

        try:

            if not self.is_trained:

                loaded = self.load_model()

                if not loaded:

                    logger.warning(
                        "ML model unavailable. Using rule engine."
                    )

                    return self.rule_based_prediction(
                        current_metrics,
                        recent_metrics
                    )

            feature_vector = self.create_feature_vector(
                current_metrics
            )

            scaled = self.scaler.transform([feature_vector])

            probability = self.model.predict_proba(scaled)[0][1]

            failure_probability = round(
                probability * 100,
                2
            )

            severity = "normal"

            if failure_probability > 75:
                severity = "critical"

            elif failure_probability > 45:
                severity = "warning"

            risk_factors = self.detect_risk_factors(
                current_metrics
            )

            recommendation = self.get_recommendation(
                failure_probability
            )

            return {
                'status': 'success',
                'prediction_method': 'machine_learning',
                'failure_probability': failure_probability,
                'severity': severity,
                'risk_factors': risk_factors,
                'recommendation': recommendation,
                'confidence': round(
                    max(probability, 1 - probability),
                    3
                ),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(f"ML prediction failed: {e}")

            return self.rule_based_prediction(
                current_metrics,
                recent_metrics
            )

    def create_feature_vector(self, metrics):

        cpu = metrics.get('cpu_usage', 0)

        memory = metrics.get('memory_usage', 0)

        disk = metrics.get('disk_usage', 0)

        load1 = metrics.get('load_1min', 0)

        load5 = metrics.get('load_5min', 0)

        network_errors = (
            metrics.get('network_rx_errors', 0)
            + metrics.get('network_tx_errors', 0)
        )

        cpu_memory_ratio = cpu / (memory + 1)

        system_pressure = (
            cpu + memory + disk
        ) / 3

        return [
            cpu,
            memory,
            disk,
            load1,
            load5,
            network_errors,
            cpu_memory_ratio,
            system_pressure
        ]

    def rule_based_prediction(
        self,
        current_metrics,
        recent_metrics=None
    ):

        cpu = current_metrics.get('cpu_usage', 0)

        memory = current_metrics.get('memory_usage', 0)

        disk = current_metrics.get('disk_usage', 0)

        load = current_metrics.get('load_1min', 0)

        risk_score = 0

        risk_factors = []

        if cpu > 90:
            risk_score += 25
            risk_factors.append("CPU overload")

        if memory > 90:
            risk_score += 25
            risk_factors.append("Memory overload")

        if disk > 95:
            risk_score += 20
            risk_factors.append("Disk almost full")

        if load > 8:
            risk_score += 20
            risk_factors.append("System load high")

        if recent_metrics and len(recent_metrics) >= 5:

            cpu_trend = self.calculate_trend(
                [m.get('cpu_usage', 0)
                 for m in recent_metrics]
            )

            if cpu_trend > 3:
                risk_score += 10
                risk_factors.append(
                    "Rapid CPU increase"
                )

        failure_probability = min(risk_score, 100)

        severity = "normal"

        if failure_probability > 70:
            severity = "critical"

        elif failure_probability > 40:
            severity = "warning"

        return {
            'status': 'success',
            'prediction_method': 'rule_based',
            'failure_probability': failure_probability,
            'severity': severity,
            'risk_factors': risk_factors,
            'recommendation': self.get_recommendation(
                failure_probability
            ),
            'timestamp': datetime.now().isoformat()
        }

    def calculate_trend(self, values):

        if len(values) < 2:
            return 0

        x = np.arange(len(values))

        slope, intercept = np.polyfit(x, values, 1)

        return slope

    def detect_risk_factors(self, metrics):

        risks = []

        if metrics.get('cpu_usage', 0) > 80:
            risks.append("High CPU usage")

        if metrics.get('memory_usage', 0) > 80:
            risks.append("High memory usage")

        if metrics.get('disk_usage', 0) > 85:
            risks.append("Disk pressure")

        if metrics.get('load_1min', 0) > 5:
            risks.append("High load average")

        if len(risks) == 0:
            risks.append("System stable")

        return risks

    def get_recommendation(self, probability):

        if probability > 80:

            return (
                "URGENT: Scale infrastructure immediately "
                "or restart services"
            )

        elif probability > 50:

            return (
                "Monitor system closely and prepare scaling"
            )

        else:

            return (
                "System operating normally"
            )

    def save_model(self):

        joblib.dump(
            self.model,
            f'{self.model_dir}/failure_predictor.pkl'
        )

        joblib.dump(
            self.scaler,
            f'{self.model_dir}/failure_scaler.pkl'
        )

        logger.info("Failure prediction model saved")

    def load_model(self):

        try:

            self.model = joblib.load(
                f'{self.model_dir}/failure_predictor.pkl'
            )

            self.scaler = joblib.load(
                f'{self.model_dir}/failure_scaler.pkl'
            )

            self.is_trained = True

            logger.info("Failure model loaded")

            return True

        except Exception as e:

            logger.error(f"Load model failed: {e}")

            return False


failure_predictor = FailurePredictor()














# """
# System Failure Prediction
# """
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# import joblib
# import os
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)


# class FailurePredictor:
#     """Predict potential system failures"""
    
#     def __init__(self, model_dir='ml_data/models'):
#         self.model_dir = model_dir
#         self.model = None
#         os.makedirs(model_dir, exist_ok=True)
    
#     def prepare_features(self, metrics):
#         """Prepare features for prediction"""
#         return np.array([[
#             metrics.get('cpu_usage', 0),
#             metrics.get('memory_usage', 0),
#             metrics.get('disk_usage', 0),
#             metrics.get('load_1min', 0),
#             metrics.get('load_5min', 0),
#             metrics.get('network_rx_errors', 0) + metrics.get('network_tx_errors', 0)
#         ]])
    
#     def predict_failure(self, current_metrics, recent_metrics=None):
#         """Predict failure probability"""
        
#         # Rule-based prediction (when ML model not available)
#         cpu = current_metrics.get('cpu_usage', 0)
#         memory = current_metrics.get('memory_usage', 0)
#         disk = current_metrics.get('disk_usage', 0)
#         load = current_metrics.get('load_1min', 0)
        
#         # Calculate risk factors
#         risk_score = 0
#         risk_factors = []
        
#         if cpu > 95:
#             risk_score += 30
#             risk_factors.append('Critical CPU usage')
#         elif cpu > 85:
#             risk_score += 15
#             risk_factors.append('High CPU usage')
        
#         if memory > 95:
#             risk_score += 30
#             risk_factors.append('Critical memory usage')
#         elif memory > 85:
#             risk_score += 15
#             risk_factors.append('High memory usage')
        
#         if disk > 95:
#             risk_score += 20
#             risk_factors.append('Critical disk usage')
        
#         if load > 10:
#             risk_score += 20
#             risk_factors.append('High system load')
        
#         # Check trends if recent metrics available
#         if recent_metrics and len(recent_metrics) >= 3:
#             cpu_trend = self._calculate_trend([m.get('cpu_usage', 0) for m in recent_metrics])
#             if cpu_trend > 5:
#                 risk_score += 10
#                 risk_factors.append('Rapidly increasing CPU')
        
#         # Calculate failure probability
#         failure_probability = min(100, risk_score)
        
#         # Determine severity
#         if failure_probability >= 70:
#             severity = 'critical'
#             time_to_failure = '5-30 minutes'
#         elif failure_probability >= 40:
#             severity = 'warning'
#             time_to_failure = '30-60 minutes'
#         else:
#             severity = 'normal'
#             time_to_failure = 'No immediate risk'
        
#         return {
#             'failure_probability': failure_probability,
#             'severity': severity,
#             'risk_factors': risk_factors,
#             'estimated_time_to_failure': time_to_failure,
#             'recommendation': self._get_recommendation(failure_probability, risk_factors),
#             'timestamp': datetime.now().isoformat()
#         }
    
#     def _calculate_trend(self, values):
#         """Calculate trend slope"""
#         if len(values) < 2:
#             return 0
#         x = np.arange(len(values))
#         coeffs = np.polyfit(x, values, 1)
#         return coeffs[0]
    
#     def _get_recommendation(self, probability, risk_factors):
#         """Get recommendation based on failure probability"""
#         if probability >= 70:
#             return 'URGENT: Scale up resources immediately or restart services'
#         elif probability >= 40:
#             return 'WARNING: Monitor closely and prepare for scaling'
#         else:
#             return 'System operating normally'


# failure_predictor = FailurePredictor()
