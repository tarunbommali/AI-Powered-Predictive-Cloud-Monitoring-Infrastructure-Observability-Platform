# """
# CPU Usage Prediction using LSTM and Prophet
# """
# import numpy as np
# import pandas as pd
# try:
#     from prophet import Prophet
#     PROPHET_AVAILABLE = True
# except ImportError:
#     PROPHET_AVAILABLE = False
# from sklearn.preprocessing import MinMaxScaler
# import joblib
# import os
# from datetime import datetime, timedelta
# import logging

# logger = logging.getLogger(__name__)


# class CPUPredictor:
#     """CPU usage prediction using time series models"""
    
#     def __init__(self, model_dir='ml_data/models'):
#         self.model_dir = model_dir
#         self.prophet_model = None
#         self.scaler = MinMaxScaler()
#         os.makedirs(model_dir, exist_ok=True)
    
#     def prepare_data(self, historical_data):
#         """Prepare data for Prophet"""
#         df = pd.DataFrame(historical_data)
        
#         # Convert to Prophet format
#         prophet_df = pd.DataFrame({
#             'ds': pd.to_datetime(df['timestamp']),
#             'y': df['cpu_usage']
#         })
        
#         return prophet_df
    
#     def train(self, historical_data):
#         """Train Prophet model for CPU prediction"""
#         if not PROPHET_AVAILABLE:
#             return {'status': 'error', 'message': 'Prophet library not installed. Install with: pip install prophet'}
        
#         logger.info("Training CPU prediction model...")
        
#         df = self.prepare_data(historical_data)
        
#         # Initialize and train Prophet
#         self.prophet_model = Prophet(
#             daily_seasonality=True,
#             weekly_seasonality=True,
#             changepoint_prior_scale=0.05
#         )
#         self.prophet_model.fit(df)
        
#         # Save model
#         self.save_model()
        
#         logger.info("CPU prediction model trained successfully")
        
#         return {
#             'status': 'success',
#             'samples_trained': len(df)
#         }
    
#     def predict(self, minutes_ahead=30):
#         """Predict CPU usage for next N minutes"""
#         if self.prophet_model is None:
#             self.load_model()
#             if self.prophet_model is None:
#                 return {'error': 'Model not trained'}
        
#         # Create future dataframe
#         future = self.prophet_model.make_future_dataframe(
#             periods=minutes_ahead,
#             freq='T'  # minute frequency
#         )
        
#         # Make predictions
#         forecast = self.prophet_model.predict(future)
        
#         # Get predictions for future only
#         predictions = forecast.tail(minutes_ahead)
        
#         result = []
#         for _, row in predictions.iterrows():
#             result.append({
#                 'timestamp': row['ds'].isoformat(),
#                 'predicted_cpu': max(0, min(100, row['yhat'])),  # Clamp to 0-100
#                 'lower_bound': max(0, row['yhat_lower']),
#                 'upper_bound': min(100, row['yhat_upper']),
#                 'confidence': 0.95
#             })
        
#         return {
#             'predictions': result,
#             'minutes_ahead': minutes_ahead,
#             'generated_at': datetime.now().isoformat()
#         }
    
#     def predict_next_values(self, n=10):
#         """Quick prediction for next N minutes"""
#         predictions = self.predict(minutes_ahead=n)
#         if 'error' in predictions:
#             return predictions
        
#         return predictions['predictions']
    
#     def save_model(self):
#         """Save trained model"""
#         model_path = f'{self.model_dir}/cpu_prophet_model.pkl'
#         joblib.dump(self.prophet_model, model_path)
#         logger.info(f"CPU prediction model saved to {model_path}")
    
#     def load_model(self):
#         """Load trained model"""
#         try:
#             model_path = f'{self.model_dir}/cpu_prophet_model.pkl'
#             self.prophet_model = joblib.load(model_path)
#             logger.info("CPU prediction model loaded")
#             return True
#         except Exception as e:
#             logger.error(f"Failed to load CPU model: {e}")
#             return False


# # Global instance
# cpu_predictor = CPUPredictor()





"""
CPU Usage Prediction using RandomForestRegressor
Production-friendly lightweight forecasting model
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CPUPredictor:
    """
    CPU usage prediction using RandomForestRegressor
    """

    def __init__(self, model_dir='ml_data/models'):
        self.model_dir = model_dir
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

        self.is_trained = False

        os.makedirs(model_dir, exist_ok=True)

    def prepare_data(self, historical_data):
        """
        Prepare training data with lag features
        """

        df = pd.DataFrame(historical_data)

        if len(df) < 20:
            raise ValueError("Not enough historical data")

        df['timestamp'] = pd.to_datetime(df['timestamp'])

        df = df.sort_values('timestamp')

        # Create lag features
        df['cpu_lag_1'] = df['cpu_usage'].shift(1)
        df['cpu_lag_2'] = df['cpu_usage'].shift(2)
        df['cpu_lag_3'] = df['cpu_usage'].shift(3)

        # Rolling averages
        df['cpu_mean_5'] = df['cpu_usage'].rolling(window=5).mean()
        df['cpu_mean_10'] = df['cpu_usage'].rolling(window=10).mean()

        # Time features
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute

        df = df.dropna()

        features = [
            'cpu_lag_1',
            'cpu_lag_2',
            'cpu_lag_3',
            'cpu_mean_5',
            'cpu_mean_10',
            'hour',
            'minute'
        ]

        X = df[features]

        y = df['cpu_usage']

        return X, y

    def train(self, historical_data):
        """
        Train CPU prediction model
        """

        logger.info("Training CPU prediction model...")

        try:

            X, y = self.prepare_data(historical_data)

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

            self.model.fit(X_train, y_train)

            predictions = self.model.predict(X_test)

            mae = mean_absolute_error(y_test, predictions)

            r2 = r2_score(y_test, predictions)

            self.is_trained = True

            self.save_model()

            logger.info("CPU prediction model trained successfully")

            return {
                'status': 'success',
                'samples_trained': len(X),
                'mae': round(mae, 2),
                'r2_score': round(r2, 2)
            }

        except Exception as e:

            logger.error(f"Training failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def predict(self, historical_data, minutes_ahead=30):
        """
        Predict future CPU usage
        """

        if not self.is_trained:
            loaded = self.load_model()

            if not loaded:
                return {
                    'status': 'error',
                    'message': 'Model not trained'
                }

        try:

            df = pd.DataFrame(historical_data)

            df['timestamp'] = pd.to_datetime(df['timestamp'])

            df = df.sort_values('timestamp')

            latest = df.iloc[-10:]

            cpu_values = latest['cpu_usage'].tolist()

            predictions = []

            current_time = datetime.now()

            for i in range(minutes_ahead):

                feature_row = pd.DataFrame([{
                    'cpu_lag_1': cpu_values[-1],
                    'cpu_lag_2': cpu_values[-2],
                    'cpu_lag_3': cpu_values[-3],
                    'cpu_mean_5': np.mean(cpu_values[-5:]),
                    'cpu_mean_10': np.mean(cpu_values[-10:]),
                    'hour': current_time.hour,
                    'minute': current_time.minute
                }])

                predicted_cpu = self.model.predict(feature_row)[0]

                predicted_cpu = max(0, min(100, predicted_cpu))

                predictions.append({
                    'timestamp': current_time.isoformat(),
                    'predicted_cpu': round(predicted_cpu, 2),
                    'confidence': 0.90
                })

                cpu_values.append(predicted_cpu)

                current_time += timedelta(minutes=1)

            return {
                'status': 'success',
                'predictions': predictions,
                'minutes_ahead': minutes_ahead,
                'generated_at': datetime.now().isoformat()
            }

        except Exception as e:

            logger.error(f"Prediction failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def save_model(self):
        """
        Save trained model
        """

        model_path = f'{self.model_dir}/cpu_randomforest_model.pkl'

        joblib.dump(self.model, model_path)

        logger.info(f"CPU model saved to {model_path}")

    def load_model(self):
        """
        Load trained model
        """

        try:

            model_path = f'{self.model_dir}/cpu_randomforest_model.pkl'

            self.model = joblib.load(model_path)

            self.is_trained = True

            logger.info("CPU model loaded")

            return True

        except Exception as e:

            logger.error(f"Failed to load CPU model: {e}")

            return False


# Global instance
cpu_predictor = CPUPredictor()

