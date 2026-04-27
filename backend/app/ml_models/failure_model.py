from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os


class FailureModel:
    def __init__(self, model_dir='ml_data/models'):
        self.model_path = f"{model_dir}/failure_model.pkl"
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
                m.load_1min
            ])

            # Label: failure if high usage
            if m.cpu_usage > 85 or m.memory_usage > 85:
                y.append(1)
            else:
                y.append(0)

        return np.array(X), np.array(y)

    def train(self, metrics):
        X, y = self.prepare_data(metrics)

        # 🚨 HANDLE SINGLE CLASS TRAINING
        if len(set(y)) < 2:
            # Add synthetic failure sample
            X = np.vstack([X, [95, 95, 90, 10]])
            y = np.append(y, 1)

        self.model = RandomForestClassifier(n_estimators=100)
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
            current_metrics.get('load_1min', 0)
        ]])

        probs = self.model.predict_proba(X)[0]

        # Handle single-class case safely
        if len(probs) == 1:
            prob = 0.0
        else:
            prob = probs[1]

        return {
            "failure_probability": round(prob, 3),
            "status": "critical" if prob > 0.7 else "normal"
        }


# Global instance
failure_model = FailureModel()