from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib
import os

class HealthModel:
    def __init__(self, model_dir='ml_data/models'):
        self.model_path = f"{model_dir}/health_model.pkl"
        self.model = None
        os.makedirs(model_dir, exist_ok=True)

    def prepare_data(self, metrics):
        X = []
        y = []

        for m in metrics:
            X.append([
                m.cpu_usage,
                m.memory_usage,
                m.disk_usage,
                m.network_rx,
                m.network_tx,
                m.load_1min
            ])

            # 🚨 TEMP LABEL (you can improve later)
            score = 100 - (
                m.cpu_usage * 0.3 +
                m.memory_usage * 0.3 +
                m.disk_usage * 0.2 +
                m.load_1min * 5
            )
            y.append(max(0, min(100, score)))

        return np.array(X), np.array(y)

    def train(self, metrics):
        X, y = self.prepare_data(metrics)

        self.model = RandomForestRegressor(n_estimators=100)
        self.model.fit(X, y)

        joblib.dump(self.model, self.model_path)

        return {"status": "trained", "samples": len(X)}

    def predict(self, current_metrics):
        if self.model is None:
            self.model = joblib.load(self.model_path)

        X = np.array([[
            current_metrics.get('cpu_usage', 0),
            current_metrics.get('memory_usage', 0),
            current_metrics.get('disk_usage', 0),
            current_metrics.get('network_rx', current_metrics.get('network_rx_bytes', 0)),
            current_metrics.get('network_tx', 0),
            current_metrics.get('load_1min', 0)
       ]])

        score = self.model.predict(X)[0]

        return {
            "health_score": round(score, 2)
        }


health_model = HealthModel() 