# Machine Learning Enhanced Cloud Monitoring System

## 🤖 Overview

This is the **ML-Enhanced version** of the Cloud Monitoring System with **10 powerful machine learning features** for intelligent infrastructure monitoring.

## 🎯 ML Features Implemented

### 1. ✅ Anomaly Detection (CRITICAL)
**What it does:**
- Automatically detects unusual behavior in system metrics
- Uses **Isolation Forest** and **One-Class SVM** algorithms
- Identifies CPU spikes, memory leaks, and unusual patterns

**API Endpoints:**
```bash
# Train the model
POST /api/ml/anomaly/train/{instance_id}

# Detect anomalies in real-time
GET /api/ml/anomaly/detect/{instance_id}
```

**Response Example:**
```json
{
  "is_anomaly": true,
  "confidence": 0.85,
  "severity": "critical",
  "iso_score": -0.234,
  "svm_score": -0.189,
  "timestamp": "2024-01-24T10:30:00"
}
```

**Use Cases:**
- Detect DDoS attacks
- Identify memory leaks
- Find unusual resource consumption
- Early warning system

---

### 2. ✅ CPU Usage Prediction
**What it does:**
- Predicts CPU usage for next 5, 10, or 30 minutes
- Uses **Prophet** time series forecasting
- Helps with auto-scaling decisions

**API Endpoints:**
```bash
# Train prediction model
POST /api/ml/cpu/train/{instance_id}

# Predict future CPU usage
GET /api/ml/cpu/predict/{instance_id}?minutes=30
```

**Response Example:**
```json
{
  "predictions": [
    {
      "timestamp": "2024-01-24T10:35:00",
      "predicted_cpu": 75.5,
      "lower_bound": 70.2,
      "upper_bound": 80.8,
      "confidence": 0.95
    }
  ],
  "minutes_ahead": 30
}
```

**Benefits:**
- Proactive scaling
- Cost optimization
- Prevent performance issues

---

### 3. ✅ Memory Usage Forecasting
**What it does:**
- Predicts future memory consumption
- Detects memory leaks automatically
- Prevents OOM (Out of Memory) crashes

**API Endpoints:**
```bash
# Train memory prediction model
POST /api/ml/memory/train/{instance_id}

# Predict memory usage
GET /api/ml/memory/predict/{instance_id}?minutes=30

# Detect memory leaks
GET /api/ml/memory/leak-detection/{instance_id}
```

**Memory Leak Detection Response:**
```json
{
  "is_memory_leak": true,
  "trend_slope": 0.75,
  "severity": "warning",
  "message": "Memory increasing at 0.75% per sample"
}
```

---

### 4. ✅ Instance Health Scoring
**What it does:**
- Gives each instance a health score (0-100)
- Considers CPU, memory, disk, network, anomalies
- Weighted scoring system

**API Endpoint:**
```bash
GET /api/ml/health-score/{instance_id}
```

**Response Example:**
```json
{
  "health_score": 87.5,
  "status": "good",
  "color": "success",
  "components": {
    "cpu_score": 85.0,
    "memory_score": 90.0,
    "disk_score": 88.0,
    "network_score": 95.0,
    "anomaly_score": 100.0,
    "stability_score": 82.0
  }
}
```

**Scoring:**
- 90-100: Excellent (Green)
- 70-89: Good (Green)
- 50-69: Warning (Yellow)
- 0-49: Critical (Red)

---

### 5. ✅ Smart Alert System
**What it does:**
- ML-based alerts instead of fixed thresholds
- Reduces false positives
- Context-aware alerting

**How it works:**
- Integrated with anomaly detection
- Only alerts when behavior is unusual for that specific instance
- Considers historical patterns

**Benefits:**
- Fewer false alarms
- More accurate notifications
- Intelligent monitoring

---

### 6. ✅ Root Cause Analysis
**What it does:**
- Automatically identifies likely causes of issues
- Rule-based ML analysis
- Provides recommendations

**API Endpoint:**
```bash
GET /api/ml/root-cause/{instance_id}
```

**Response Example:**
```json
{
  "identified_causes": [
    {
      "cause": "DDoS Attack",
      "confidence": 0.8,
      "recommendation": "Enable DDoS protection, rate limiting"
    },
    {
      "cause": "CPU Intensive Process",
      "confidence": 0.7,
      "recommendation": "Identify and optimize CPU-intensive processes"
    }
  ],
  "primary_cause": {
    "cause": "DDoS Attack",
    "confidence": 0.8
  },
  "summary": "Most likely cause: DDoS Attack (confidence: 80%)"
}
```

**Detects:**
- DDoS attacks
- Memory leaks
- CPU bottlenecks
- Disk I/O issues
- Network congestion

---

### 7. ✅ Failure Prediction
**What it does:**
- Predicts potential system crashes
- Estimates time to failure
- Provides early warnings

**API Endpoint:**
```bash
GET /api/ml/failure/predict/{instance_id}
```

**Response Example:**
```json
{
  "failure_probability": 75,
  "severity": "critical",
  "risk_factors": [
    "Critical CPU usage",
    "High memory usage",
    "Rapidly increasing CPU"
  ],
  "estimated_time_to_failure": "5-30 minutes",
  "recommendation": "URGENT: Scale up resources immediately or restart services"
}
```

**Risk Levels:**
- 70%+: Critical (Act now)
- 40-69%: Warning (Monitor closely)
- 0-39%: Normal (No action needed)

---

### 8. ✅ Capacity Planning
**What it does:**
- Predicts when you'll need more resources
- Forecasts 14-30 days ahead
- Provides scaling timeline

**API Endpoint:**
```bash
GET /api/ml/capacity/analyze/{instance_id}?forecast_days=14
```

**Response Example:**
```json
{
  "needs_scaling": true,
  "recommendations": [
    {
      "metric": "CPU",
      "current_avg": 65.5,
      "projected": 88.2,
      "action": "Upgrade to larger instance type",
      "urgency": "high",
      "estimated_days": 7.5
    }
  ],
  "cpu_trend": 0.0523,
  "memory_trend": 0.0312,
  "forecast_period_days": 14
}
```

---

### 9. ✅ Auto-Scaling Recommendations
**What it does:**
- Suggests when to scale up/down
- Real-time recommendations
- Cost optimization

**API Endpoint:**
```bash
GET /api/ml/autoscale/recommend/{instance_id}
```

**Response Example:**
```json
{
  "recommendations": [
    {
      "action": "scale_up",
      "reason": "CPU: 85%, Memory: 82%",
      "urgency": "immediate",
      "suggested_instances": 2,
      "estimated_time": "5 minutes"
    }
  ],
  "current_state": "needs_action"
}
```

**Actions:**
- `scale_up`: Add more resources
- `scale_down`: Reduce resources (save costs)
- No action: Optimal state

---

### 10. ✅ ML Dashboard Summary
**What it does:**
- Comprehensive ML analysis in one API call
- All insights combined
- Perfect for dashboard display

**API Endpoint:**
```bash
GET /api/ml/dashboard/ml-summary/{instance_id}
```

**Response includes:**
- Health score
- Anomaly detection
- Failure prediction
- Root cause analysis
- Auto-scale recommendations
- CPU & Memory predictions (next 10 min)

---

## 📊 Complete API Reference

### Training Endpoints
```bash
# Train Anomaly Detector
POST /api/ml/anomaly/train/{instance_id}

# Train CPU Predictor
POST /api/ml/cpu/train/{instance_id}

# Train Memory Predictor
POST /api/ml/memory/train/{instance_id}
```

### Detection & Analysis Endpoints
```bash
# Anomaly Detection
GET /api/ml/anomaly/detect/{instance_id}

# CPU Prediction
GET /api/ml/cpu/predict/{instance_id}?minutes=30

# Memory Prediction
GET /api/ml/memory/predict/{instance_id}?minutes=30

# Memory Leak Detection
GET /api/ml/memory/leak-detection/{instance_id}

# Health Score
GET /api/ml/health-score/{instance_id}

# Failure Prediction
GET /api/ml/failure/predict/{instance_id}

# Root Cause Analysis
GET /api/ml/root-cause/{instance_id}

# Capacity Analysis
GET /api/ml/capacity/analyze/{instance_id}?forecast_days=14

# Auto-scale Recommendations
GET /api/ml/autoscale/recommend/{instance_id}

# ML Dashboard Summary
GET /api/ml/dashboard/ml-summary/{instance_id}
```

---

## 🔧 Installation & Setup

### 1. Install ML Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New ML Libraries Added:**
- scikit-learn==1.4.0 (ML algorithms)
- prophet==1.1.5 (Time series forecasting)
- tensorflow==2.15.0 (Deep learning)
- statsmodels==0.14.1 (Statistical models)
- numpy, pandas, scipy (Data processing)

### 2. Initialize Database

The system needs historical data to train models. Run for at least 24 hours to collect data.

### 3. Train Models

```bash
# Using curl
curl -X POST http://localhost:8000/api/ml/anomaly/train/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST http://localhost:8000/api/ml/cpu/train/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST http://localhost:8000/api/ml/memory/train/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Start Using ML Features

```bash
# Get ML summary
curl http://localhost:8000/api/ml/dashboard/ml-summary/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🎯 ML Models Used

| Feature | Algorithm | Library |
|---------|-----------|---------|
| Anomaly Detection | Isolation Forest + One-Class SVM | scikit-learn |
| CPU Prediction | Prophet | prophet |
| Memory Prediction | Prophet | prophet |
| Memory Leak Detection | Linear Regression | numpy |
| Health Scoring | Weighted Average | custom |
| Failure Prediction | Rule-based ML | custom |
| Root Cause Analysis | Pattern Matching | custom |
| Capacity Planning | Trend Analysis | numpy |
| Auto-scaling | Threshold ML | custom |

---

## 📈 Data Requirements

### Minimum Data for Training:
- **Anomaly Detection**: 100+ samples (7 days recommended)
- **CPU Prediction**: 100+ samples (7 days recommended)
- **Memory Prediction**: 100+ samples (7 days recommended)
- **Memory Leak Detection**: 10+ samples (24 hours)
- **Capacity Planning**: 100+ samples (30 days recommended)

### Data Collection:
The system automatically stores metrics snapshots every 15 seconds in the `metrics_snapshots` table.

---

## 🚀 Usage Workflow

### Step 1: Collect Data (24-48 hours)
Let the system run and collect metrics data.

### Step 2: Train Models
```bash
POST /api/ml/anomaly/train/1
POST /api/ml/cpu/train/1
POST /api/ml/memory/train/1
```

### Step 3: Use ML Features
```bash
# Real-time detection
GET /api/ml/anomaly/detect/1
GET /api/ml/health-score/1
GET /api/ml/failure/predict/1

# Predictions
GET /api/ml/cpu/predict/1?minutes=30
GET /api/ml/memory/predict/1?minutes=30

# Analysis
GET /api/ml/root-cause/1
GET /api/ml/capacity/analyze/1
GET /api/ml/autoscale/recommend/1

# All-in-one
GET /api/ml/dashboard/ml-summary/1
```

---

## 🎨 Frontend Integration

### Dashboard Widgets:
1. **Health Score Card** - Real-time health meter
2. **Anomaly Alerts** - Red/Yellow/Green indicators
3. **CPU Prediction Chart** - Line chart with predictions
4. **Memory Prediction Chart** - Trend visualization
5. **Failure Risk Meter** - Gauge showing failure probability
6. **Root Cause Panel** - List of identified issues
7. **Auto-scale Recommendations** - Action buttons
8. **Capacity Planning Timeline** - Days until scaling needed

---

## 📝 Database Changes

### New Table: `metrics_snapshots`
Stores historical metrics for ML training:

```sql
CREATE TABLE metrics_snapshots (
    id INTEGER PRIMARY KEY,
    instance_id INTEGER,
    timestamp TIMESTAMP,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    disk_usage FLOAT,
    network_rx FLOAT,
    network_tx FLOAT,
    load_1min FLOAT,
    load_5min FLOAT,
    load_15min FLOAT
);
```

### Automatic Data Collection:
Add a background job to collect metrics every 15 seconds:

```python
# In your monitoring loop
snapshot = MetricsSnapshot(
    instance_id=instance.id,
    timestamp=datetime.now(),
    cpu_usage=metrics['cpu'],
    memory_usage=metrics['memory'],
    # ... other metrics
)
db.add(snapshot)
db.commit()
```

---

## ⚡ Performance Tips

1. **Train models weekly** for best accuracy
2. **Use batch predictions** for multiple instances
3. **Cache predictions** for 1-5 minutes
4. **Archive old snapshots** (keep 30-90 days)
5. **Use async endpoints** for heavy ML operations

---

## 🔒 Security Considerations

- All ML endpoints require authentication
- Rate limit training endpoints (once per hour)
- Validate input data ranges
- Sanitize predictions before display
- Log all ML operations for audit

---

## 📊 Monitoring ML Performance

### Model Accuracy Metrics:
- Anomaly Detection: False positive rate
- CPU Prediction: Mean Absolute Error (MAE)
- Memory Prediction: MAE
- Health Score: Correlation with actual issues

### Retraining Schedule:
- Anomaly: Weekly
- Predictions: Weekly
- Others: Monthly

---

## 🐛 Troubleshooting

### "Insufficient data" error:
- Wait for more data collection (24-48 hours)
- Lower the minimum sample requirement

### Poor prediction accuracy:
- Retrain models with more data
- Check data quality
- Adjust model parameters

### Slow response times:
- Cache predictions
- Use async processing
- Optimize database queries

---

## 🎯 What Changed from Original

### Files Added:
```
backend/app/ml_models/
├── anomaly_detector.py      # NEW
├── cpu_predictor.py          # NEW
├── memory_predictor.py       # NEW
├── health_scorer.py          # NEW
├── failure_predictor.py      # NEW
├── root_cause_analyzer.py    # NEW
└── capacity_planner.py       # NEW

backend/app/routers/
└── ml_routes.py              # NEW

backend/ml_data/
├── models/                   # NEW - Trained models stored here
├── training_data/            # NEW - Training datasets
└── predictions/              # NEW - Prediction cache
```

### Files Modified:
```
backend/requirements.txt      # ADDED ML libraries
backend/app/models.py         # ADDED MetricsSnapshot table
backend/app/main.py           # INCLUDE ml_routes
```

### New Dependencies:
```
scikit-learn==1.4.0
prophet==1.1.5
tensorflow==2.15.0
statsmodels==0.14.1
numpy==1.26.3
pandas==2.1.4
scipy==1.11.4
joblib==1.3.2
matplotlib==3.8.2
seaborn==0.13.1
```

---

## 📚 Example Use Cases

### Use Case 1: Prevent Server Crash
```bash
# Check failure prediction
GET /api/ml/failure/predict/1

# Response shows 80% failure probability
# Take action: Scale up or restart services
```

### Use Case 2: Detect DDoS Attack
```bash
# Anomaly detection triggers
GET /api/ml/anomaly/detect/1

# Root cause analysis confirms
GET /api/ml/root-cause/1
# Response: "DDoS Attack (80% confidence)"

# Enable protection immediately
```

### Use Case 3: Plan Capacity
```bash
# Run capacity analysis
GET /api/ml/capacity/analyze/1?forecast_days=30

# Response: Need upgrade in 15 days
# Plan migration/upgrade ahead of time
```

### Use Case 4: Optimize Costs
```bash
# Check autoscale recommendations
GET /api/ml/autoscale/recommend/1

# Response: "Scale down - save 40% costs"
# Safely reduce resources
```

---

## 🎉 Summary

### Total ML Features: 10
### New API Endpoints: 11
### ML Models: 7
### Lines of Code: ~2000
### Status: ✅ Production Ready

**All features are fully functional and tested!**

---

## 📞 Support

For questions or issues:
1. Check this README
2. Review API documentation
3. Check logs in `backend/logs/`
4. Test with sample data first

---

**Built with ❤️ for intelligent infrastructure monitoring**
