"""
Anomaly Detection using Isolation Forest and One-Class SVM
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Multi-model anomaly detection system"""
    
    def __init__(self, model_dir='ml_data/models'):
        self.model_dir = model_dir
        self.scaler = StandardScaler()
        self.isolation_forest = None
        self.one_class_svm = None
        os.makedirs(model_dir, exist_ok=True)
    
    def prepare_features(self, metrics_data):
        """Prepare features from metrics data"""
        df = pd.DataFrame(metrics_data)
        
        features = []
        for _, row in df.iterrows():
            feature_vector = [
                row.get('cpu_usage', 0),
                row.get('memory_usage', 0),
                row.get('disk_usage', 0),
                row.get('network_rx', 0),
                row.get('network_tx', 0),
                row.get('load_1min', 0),
                row.get('load_5min', 0),
                row.get('load_15min', 0),
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train(self, historical_data, contamination=0.1):
        """Train anomaly detection models"""
        logger.info("Training anomaly detection models...")
        
        X = self.prepare_features(historical_data)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.isolation_forest.fit(X_scaled)
        
        # Train One-Class SVM
        self.one_class_svm = OneClassSVM(
            kernel='rbf',
            gamma='auto',
            nu=contamination
        )
        self.one_class_svm.fit(X_scaled)
        
        # Save models
        self.save_models()
        
        logger.info("Anomaly detection models trained successfully")
        
        return {
            'status': 'success',
            'samples_trained': len(X),
            'features': X.shape[1]
        }
    
    def detect(self, current_metrics):
        """Detect anomalies in current metrics"""
        if self.isolation_forest is None or self.one_class_svm is None:
            self.load_models()
            if self.isolation_forest is None:
                return {'is_anomaly': False, 'confidence': 0, 'message': 'Models not trained'}
        
        # Prepare features
        features = self.prepare_features([current_metrics])
        features_scaled = self.scaler.transform(features)
        
        # Get predictions from both models
        iso_pred = self.isolation_forest.predict(features_scaled)[0]
        svm_pred = self.one_class_svm.predict(features_scaled)[0]
        
        # Get anomaly scores
        iso_score = self.isolation_forest.score_samples(features_scaled)[0]
        svm_score = self.one_class_svm.score_samples(features_scaled)[0]
        
        # Combine predictions (both must agree for anomaly)
        is_anomaly = (iso_pred == -1 or svm_pred == -1)
        
        # Calculate confidence (normalized)
        confidence = abs(iso_score) * 0.5 + abs(svm_score) * 0.5
        
        # Determine severity
        severity = 'normal'
        if is_anomaly:
            if confidence > 0.7:
                severity = 'critical'
            elif confidence > 0.4:
                severity = 'warning'
            else:
                severity = 'minor'
        
        return {
            'is_anomaly': bool(is_anomaly),
            'confidence': float(confidence),
            'severity': severity,
            'iso_score': float(iso_score),
            'svm_score': float(svm_score),
            'timestamp': datetime.now().isoformat()
        }
    
    def save_models(self):
        """Save trained models"""
        joblib.dump(self.scaler, f'{self.model_dir}/anomaly_scaler.pkl')
        joblib.dump(self.isolation_forest, f'{self.model_dir}/isolation_forest.pkl')
        joblib.dump(self.one_class_svm, f'{self.model_dir}/one_class_svm.pkl')
        logger.info("Anomaly detection models saved")
    
    def load_models(self):
        """Load trained models"""
        try:
            self.scaler = joblib.load(f'{self.model_dir}/anomaly_scaler.pkl')
            self.isolation_forest = joblib.load(f'{self.model_dir}/isolation_forest.pkl')
            self.one_class_svm = joblib.load(f'{self.model_dir}/one_class_svm.pkl')
            logger.info("Anomaly detection models loaded")
            return True
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            return False


# Global instance
anomaly_detector = AnomalyDetector()
