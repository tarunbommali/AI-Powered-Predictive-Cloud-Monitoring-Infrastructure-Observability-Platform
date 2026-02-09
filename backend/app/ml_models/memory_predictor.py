"""
Memory Usage Forecasting
"""
import numpy as np
import pandas as pd
from prophet import Prophet
import joblib
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MemoryPredictor:
    """Memory usage prediction and leak detection"""
    
    def __init__(self, model_dir='ml_data/models'):
        self.model_dir = model_dir
        self.prophet_model = None
        os.makedirs(model_dir, exist_ok=True)
    
    def train(self, historical_data):
        """Train Prophet model for memory prediction"""
        logger.info("Training memory prediction model...")
        
        df = pd.DataFrame(historical_data)
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df['timestamp']),
            'y': df['memory_usage']
        })
        
        self.prophet_model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=False,
            changepoint_prior_scale=0.1
        )
        self.prophet_model.fit(prophet_df)
        self.save_model()
        
        return {'status': 'success', 'samples': len(df)}
    
    def predict(self, minutes_ahead=30):
        """Predict memory usage"""
        if self.prophet_model is None:
            self.load_model()
        
        future = self.prophet_model.make_future_dataframe(periods=minutes_ahead, freq='T')
        forecast = self.prophet_model.predict(future)
        predictions = forecast.tail(minutes_ahead)
        
        result = [{
            'timestamp': row['ds'].isoformat(),
            'predicted_memory': max(0, min(100, row['yhat'])),
            'lower_bound': max(0, row['yhat_lower']),
            'upper_bound': min(100, row['yhat_upper'])
        } for _, row in predictions.iterrows()]
        
        return {'predictions': result, 'minutes_ahead': minutes_ahead}
    
    def detect_memory_leak(self, historical_data, threshold=0.5):
        """Detect potential memory leaks"""
        df = pd.DataFrame(historical_data)
        df = df.sort_values('timestamp')
        
        # Calculate trend
        memory_values = df['memory_usage'].values
        time_indices = np.arange(len(memory_values))
        
        # Linear regression
        coefficients = np.polyfit(time_indices, memory_values, 1)
        slope = coefficients[0]
        
        # Check for consistent increase
        is_leak = slope > threshold
        
        return {
            'is_memory_leak': bool(is_leak),
            'trend_slope': float(slope),
            'severity': 'critical' if slope > 1.0 else 'warning' if slope > 0.5 else 'normal',
            'message': f'Memory increasing at {slope:.2f}% per sample' if is_leak else 'No memory leak detected'
        }
    
    def save_model(self):
        joblib.dump(self.prophet_model, f'{self.model_dir}/memory_prophet_model.pkl')
    
    def load_model(self):
        try:
            self.prophet_model = joblib.load(f'{self.model_dir}/memory_prophet_model.pkl')
            return True
        except:
            return False


memory_predictor = MemoryPredictor()
