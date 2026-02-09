# Quick Start - ML Features

## 🚀 Get Started in 5 Minutes

### Step 1: Install (1 minute)
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend (30 seconds)
```bash
uvicorn app.main:app --reload
```

### Step 3: Wait for Data (24 hours)
The system collects metrics automatically. Come back tomorrow!

### Step 4: Train Models (2 minutes)
```bash
# Get your auth token first
TOKEN="your-jwt-token"

# Train all models
curl -X POST http://localhost:8000/api/ml/anomaly/train/1 \
  -H "Authorization: Bearer $TOKEN"

curl -X POST http://localhost:8000/api/ml/cpu/train/1 \
  -H "Authorization: Bearer $TOKEN"

curl -X POST http://localhost:8000/api/ml/memory/train/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Step 5: Use ML Features (30 seconds)
```bash
# Get everything in one call
curl http://localhost:8000/api/ml/dashboard/ml-summary/1 \
  -H "Authorization: Bearer $TOKEN" | jq
```

## 🎯 Test Individual Features

### Anomaly Detection
```bash
curl http://localhost:8000/api/ml/anomaly/detect/1 \
  -H "Authorization: Bearer $TOKEN"
```

### CPU Prediction
```bash
curl http://localhost:8000/api/ml/cpu/predict/1?minutes=30 \
  -H "Authorization: Bearer $TOKEN"
```

### Health Score
```bash
curl http://localhost:8000/api/ml/health-score/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Failure Prediction
```bash
curl http://localhost:8000/api/ml/failure/predict/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Root Cause Analysis
```bash
curl http://localhost:8000/api/ml/root-cause/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Auto-scale Recommendations
```bash
curl http://localhost:8000/api/ml/autoscale/recommend/1 \
  -H "Authorization: Bearer $TOKEN"
```

## 🎨 Example Responses

### Health Score Response:
```json
{
  "health_score": 87.5,
  "status": "good",
  "color": "success",
  "components": {
    "cpu_score": 85.0,
    "memory_score": 90.0,
    "disk_score": 88.0
  }
}
```

### Anomaly Detection Response:
```json
{
  "is_anomaly": true,
  "confidence": 0.85,
  "severity": "critical",
  "message": "Unusual behavior detected"
}
```

### CPU Prediction Response:
```json
{
  "predictions": [
    {
      "timestamp": "2024-01-24T10:35:00",
      "predicted_cpu": 75.5,
      "confidence": 0.95
    }
  ]
}
```

## ✅ That's It!

You now have:
- ✅ Anomaly detection
- ✅ CPU & memory predictions
- ✅ Health scoring
- ✅ Failure prediction
- ✅ Root cause analysis
- ✅ Auto-scale recommendations

**All working automatically!** 🎉
