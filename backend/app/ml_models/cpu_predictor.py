"""
CPU Usage Prediction using LSTM and Prophet
"""
import numpy as np
import pandas as pd
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CPUPredictor:
    """CPU usage prediction using time series models"""
    
    def __init__(self, model_dir='ml_data/models'):
        self.model_dir = model_dir
        self.prophet_model = None
        self.scaler = MinMaxScaler()
        os.makedirs(model_dir, exist_ok=True)
    
    def prepare_data(self, historical_data):
        """Prepare data for Prophet"""
        df = pd.DataFrame(historical_data)
        
        # Convert to Prophet format
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df['timestamp']),
            'y': df['cpu_usage']
        })
        
        return prophet_df
    
    def train(self, historical_data):
        """Train Prophet model for CPU prediction"""
        if not PROPHET_AVAILABLE:
            return {'status': 'error', 'message': 'Prophet library not installed. Install with: pip install prophet'}
        
        logger.info("Training CPU prediction model...")
        
        df = self.prepare_data(historical_data)
        
        # Initialize and train Prophet
        self.prophet_model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        self.prophet_model.fit(df)
        
        # Save model
        self.save_model()
        
        logger.info("CPU prediction model trained successfully")
        
        return {
            'status': 'success',
            'samples_trained': len(df)
        }
    
    def predict(self, minutes_ahead=30):
        """Predict CPU usage for next N minutes"""
        if self.prophet_model is None:
            self.load_model()
            if self.prophet_model is None:
                return {'error': 'Model not trained'}
        
        # Create future dataframe
        future = self.prophet_model.make_future_dataframe(
            periods=minutes_ahead,
            freq='T'  # minute frequency
        )
        
        # Make predictions
        forecast = self.prophet_model.predict(future)
        
        # Get predictions for future only
        predictions = forecast.tail(minutes_ahead)
        
        result = []
        for _, row in predictions.iterrows():
            result.append({
                'timestamp': row['ds'].isoformat(),
                'predicted_cpu': max(0, min(100, row['yhat'])),  # Clamp to 0-100
                'lower_bound': max(0, row['yhat_lower']),
                'upper_bound': min(100, row['yhat_upper']),
                'confidence': 0.95
            })
        
        return {
            'predictions': result,
            'minutes_ahead': minutes_ahead,
            'generated_at': datetime.now().isoformat()
        }
    
    def predict_next_values(self, n=10):
        """Quick prediction for next N minutes"""
        predictions = self.predict(minutes_ahead=n)
        if 'error' in predictions:
            return predictions
        
        return predictions['predictions']
    
    def save_model(self):
        """Save trained model"""
        model_path = f'{self.model_dir}/cpu_prophet_model.pkl'
        joblib.dump(self.prophet_model, model_path)
        logger.info(f"CPU prediction model saved to {model_path}")
    
    def load_model(self):
        """Load trained model"""
        try:
            model_path = f'{self.model_dir}/cpu_prophet_model.pkl'
            self.prophet_model = joblib.load(model_path)
            logger.info("CPU prediction model loaded")
            return True
        except Exception as e:
            logger.error(f"Failed to load CPU model: {e}")
            return False


# Global instance
cpu_predictor = CPUPredictor()
