
"""
Memory Usage Forecasting using RandomForest
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MemoryPredictor:
    """
    Memory prediction + leak detection
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

        df = pd.DataFrame(historical_data)

        if len(df) < 20:
            raise ValueError("Not enough training data")

        df['timestamp'] = pd.to_datetime(df['timestamp'])

        df = df.sort_values('timestamp')

        # Lag features
        df['mem_lag_1'] = df['memory_usage'].shift(1)
        df['mem_lag_2'] = df['memory_usage'].shift(2)
        df['mem_lag_3'] = df['memory_usage'].shift(3)

        # Rolling features
        df['mem_mean_5'] = df['memory_usage'].rolling(5).mean()
        df['mem_mean_10'] = df['memory_usage'].rolling(10).mean()

        # Time features
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute

        df = df.dropna()

        features = [
            'mem_lag_1',
            'mem_lag_2',
            'mem_lag_3',
            'mem_mean_5',
            'mem_mean_10',
            'hour',
            'minute'
        ]

        X = df[features]

        y = df['memory_usage']

        return X, y

    def train(self, historical_data):

        logger.info("Training memory prediction model...")

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

            self.is_trained = True

            self.save_model()

            return {
                'status': 'success',
                'samples_trained': len(X),
                'mae': round(mae, 2)
            }

        except Exception as e:

            logger.error(f"Training failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def predict(self, historical_data, minutes_ahead=30):

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

            memory_values = latest['memory_usage'].tolist()

            predictions = []

            current_time = datetime.now()

            for i in range(minutes_ahead):

                feature_row = pd.DataFrame([{
                    'mem_lag_1': memory_values[-1],
                    'mem_lag_2': memory_values[-2],
                    'mem_lag_3': memory_values[-3],
                    'mem_mean_5': np.mean(memory_values[-5:]),
                    'mem_mean_10': np.mean(memory_values[-10:]),
                    'hour': current_time.hour,
                    'minute': current_time.minute
                }])

                predicted_memory = self.model.predict(feature_row)[0]

                predicted_memory = max(0, min(100, predicted_memory))

                predictions.append({
                    'timestamp': current_time.isoformat(),
                    'predicted_memory': round(predicted_memory, 2),
                    'confidence': 0.90
                })

                memory_values.append(predicted_memory)

                current_time += timedelta(minutes=1)

            return {
                'status': 'success',
                'predictions': predictions,
                'minutes_ahead': minutes_ahead
            }

        except Exception as e:

            logger.error(f"Prediction failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def detect_memory_leak(self, historical_data, threshold=0.3):
        """
        Detect gradual memory increase
        """

        try:

            df = pd.DataFrame(historical_data)

            df = df.sort_values('timestamp')

            memory_values = df['memory_usage'].values

            if len(memory_values) < 10:

                return {
                    'status': 'error',
                    'message': 'Not enough data'
                }

            x = np.arange(len(memory_values))

            slope, intercept = np.polyfit(x, memory_values, 1)

            avg_growth = slope

            is_leak = avg_growth > threshold

            severity = "normal"

            if avg_growth > 1.0:
                severity = "critical"

            elif avg_growth > 0.5:
                severity = "warning"

            return {
                'status': 'success',
                'is_memory_leak': bool(is_leak),
                'growth_rate': round(float(avg_growth), 4),
                'severity': severity,
                'message': (
                    f"Possible memory leak detected. Growth rate: {avg_growth:.2f}"
                    if is_leak
                    else "Memory usage stable"
                )
            }

        except Exception as e:

            logger.error(f"Memory leak detection failed: {e}")

            return {
                'status': 'error',
                'message': str(e)
            }

    def save_model(self):

        model_path = f'{self.model_dir}/memory_randomforest_model.pkl'

        joblib.dump(self.model, model_path)

        logger.info(f"Memory model saved to {model_path}")

    def load_model(self):

        try:

            model_path = f'{self.model_dir}/memory_randomforest_model.pkl'

            self.model = joblib.load(model_path)

            self.is_trained = True

            logger.info("Memory model loaded")

            return True

        except Exception as e:

            logger.error(f"Failed to load memory model: {e}")

            return False


memory_predictor = MemoryPredictor()






# """
# Memory Usage Forecasting
# """
# import numpy as np
# import pandas as pd
# try:
#     from prophet import Prophet
#     PROPHET_AVAILABLE = True
# except ImportError:
#     PROPHET_AVAILABLE = False
# import joblib
# import os
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)


# class MemoryPredictor:
#     """Memory usage prediction and leak detection"""
    
#     def __init__(self, model_dir='ml_data/models'):
#         self.model_dir = model_dir
#         self.prophet_model = None
#         os.makedirs(model_dir, exist_ok=True)
    
#     def train(self, historical_data):
#         """Train Prophet model for memory prediction"""
#         if not PROPHET_AVAILABLE:
#             return {'status': 'error', 'message': 'Prophet library not installed. Install with: pip install prophet'}
        
#         logger.info("Training memory prediction model...")
        
#         df = pd.DataFrame(historical_data)
#         prophet_df = pd.DataFrame({
#             'ds': pd.to_datetime(df['timestamp']),
#             'y': df['memory_usage']
#         })
        
#         self.prophet_model = Prophet(
#             daily_seasonality=True,
#             weekly_seasonality=False,
#             changepoint_prior_scale=0.1
#         )
#         self.prophet_model.fit(prophet_df)
#         self.save_model()
        
#         return {'status': 'success', 'samples': len(df)}
    
#     def predict(self, minutes_ahead=30):
#         """Predict memory usage"""
#         if self.prophet_model is None:
#             self.load_model()
        
#         future = self.prophet_model.make_future_dataframe(periods=minutes_ahead, freq='T')
#         forecast = self.prophet_model.predict(future)
#         predictions = forecast.tail(minutes_ahead)
        
#         result = [{
#             'timestamp': row['ds'].isoformat(),
#             'predicted_memory': max(0, min(100, row['yhat'])),
#             'lower_bound': max(0, row['yhat_lower']),
#             'upper_bound': min(100, row['yhat_upper'])
#         } for _, row in predictions.iterrows()]
        
#         return {'predictions': result, 'minutes_ahead': minutes_ahead}
    
#     def detect_memory_leak(self, historical_data, threshold=0.5):
#         """Detect potential memory leaks"""
#         df = pd.DataFrame(historical_data)
#         df = df.sort_values('timestamp')
        
#         # Calculate trend
#         memory_values = df['memory_usage'].values
#         time_indices = np.arange(len(memory_values))
        
#         # Linear regression
#         coefficients = np.polyfit(time_indices, memory_values, 1)
#         slope = coefficients[0]
        
#         # Check for consistent increase
#         is_leak = slope > threshold
        
#         return {
#             'is_memory_leak': bool(is_leak),
#             'trend_slope': float(slope),
#             'severity': 'critical' if slope > 1.0 else 'warning' if slope > 0.5 else 'normal',
#             'message': f'Memory increasing at {slope:.2f}% per sample' if is_leak else 'No memory leak detected'
#         }
    
#     def save_model(self):
#         joblib.dump(self.prophet_model, f'{self.model_dir}/memory_prophet_model.pkl')
    
#     def load_model(self):
#         try:
#             self.prophet_model = joblib.load(f'{self.model_dir}/memory_prophet_model.pkl')
#             return True
#         except:
#             return False


# memory_predictor = MemoryPredictor()




