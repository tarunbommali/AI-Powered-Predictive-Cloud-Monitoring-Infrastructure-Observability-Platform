# Backend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already created with default settings. You can modify it if needed:

```bash
# Edit .env file
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 3. Start the Backend

```bash
# Option 1: Using the startup script (recommended)
python start_backend.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Create Dummy Users

In a new terminal (keep the backend running):

```bash
cd backend
python create_dummy_users.py
```

This will create 3 test users:
- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`user`, password=`user123`
- **Demo**: username=`demo`, password=`demo123`

### 5. Access the API

- **API Documentation**: http://localhost:8000/api/docs
- **Alternative Docs**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/health

## Dependencies Overview

### Web Framework & API
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations

### Authentication & Security
- **python-jose**: JWT token creation and validation
- **passlib**: Password hashing with bcrypt
- **email-validator**: Email validation

### Database & ORM
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **psycopg2-binary**: PostgreSQL adapter (optional)
- **asyncpg**: Async PostgreSQL driver (optional)

### ML Libraries
- **scikit-learn**: Machine learning algorithms (Isolation Forest, SVM)
- **Prophet**: Time series forecasting (CPU/Memory prediction)
- **TensorFlow**: Deep learning framework (Failure prediction)
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **scipy**: Scientific computing
- **statsmodels**: Statistical models
- **joblib**: Model serialization
- **matplotlib**: Plotting library
- **seaborn**: Statistical data visualization

### Monitoring & Services
- **prometheus-client**: Prometheus metrics integration
- **requests**: HTTP library for API calls
- **aiohttp**: Async HTTP client/server
- **redis**: Redis client (optional)
- **celery**: Distributed task queue (optional)

### Utilities
- **python-dotenv**: Environment variable management

## ML Features

The backend includes 10 ML-powered features:

1. **Anomaly Detection** - Isolation Forest + One-Class SVM
2. **CPU Usage Prediction** - Prophet time series forecasting
3. **Memory Usage Forecasting** - Prophet forecasting
4. **Memory Leak Detection** - Trend analysis
5. **Health Scoring** - Weighted scoring system (0-100)
6. **Failure Prediction** - Neural network + rule-based
7. **Root Cause Analysis** - Pattern-based ML logic
8. **Capacity Planning** - 14-30 day forecasting
9. **Auto-Scaling Recommendations** - Decision logic + predictions
10. **ML Dashboard Summary** - Comprehensive ML insights

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user info

### Health
- `GET /api/health` - Basic health check
- `GET /api/health/services` - Check all services

### Instances
- `GET /api/instances` - List all instances
- `POST /api/instances` - Add new instance
- `GET /api/instances/{id}` - Get instance details
- `PUT /api/instances/{id}` - Update instance
- `DELETE /api/instances/{id}` - Delete instance

### Metrics
- `GET /api/metrics/cpu/{instance_id}` - CPU metrics
- `GET /api/metrics/memory/{instance_id}` - Memory metrics
- `GET /api/metrics/disk/{instance_id}` - Disk metrics
- `GET /api/metrics/network/{instance_id}` - Network metrics
- `GET /api/metrics/all/{instance_id}` - All metrics

### ML Features
- `POST /api/ml/anomaly/train/{instance_id}` - Train anomaly detector
- `GET /api/ml/anomaly/detect/{instance_id}` - Detect anomalies
- `POST /api/ml/cpu/train/{instance_id}` - Train CPU predictor
- `GET /api/ml/cpu/predict/{instance_id}` - Predict CPU usage
- `POST /api/ml/memory/train/{instance_id}` - Train memory predictor
- `GET /api/ml/memory/predict/{instance_id}` - Predict memory usage
- `GET /api/ml/memory/leak-detection/{instance_id}` - Detect memory leaks
- `GET /api/ml/health-score/{instance_id}` - Get health score
- `GET /api/ml/failure/predict/{instance_id}` - Predict failures
- `GET /api/ml/root-cause/{instance_id}` - Analyze root cause
- `GET /api/ml/capacity/analyze/{instance_id}` - Capacity planning
- `GET /api/ml/autoscale/recommend/{instance_id}` - Auto-scale recommendations
- `GET /api/ml/dashboard/ml-summary/{instance_id}` - ML dashboard summary

## Testing the API

### 1. Login to get token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 2. Use token for authenticated requests

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Database Errors

If you get database errors, delete the database file and restart:

```bash
rm monitoring.db
python start_backend.py
```

### Port Already in Use

If port 8000 is already in use, change it in `start_backend.py` or use:

```bash
uvicorn app.main:app --reload --port 8001
```

### ML Model Errors

ML models require training data. If you get "Model not trained" errors:
1. Add some instances to the system
2. Wait for metrics to be collected
3. Train the models using the training endpoints

## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── health.py
│   │   ├── instances.py
│   │   ├── metrics.py
│   │   └── ml_routes.py
│   ├── services/            # Business logic services
│   │   ├── prometheus.py
│   │   └── alerting.py
│   └── ml_models/           # ML model implementations
│       ├── anomaly_detector.py
│       ├── cpu_predictor.py
│       ├── memory_predictor.py
│       ├── health_scorer.py
│       ├── failure_predictor.py
│       ├── root_cause_analyzer.py
│       └── capacity_planner.py
├── ml_data/
│   └── models/              # Trained ML models
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── start_backend.py         # Startup script
└── create_dummy_users.py    # User creation script
```

### Adding New Features

1. Create new router in `app/routers/`
2. Add route to `app/main.py`
3. Create schemas in `app/schemas.py`
4. Add models in `app/models.py` if needed

## Production Deployment

For production deployment:

1. Change `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Set up proper CORS origins
5. Configure email alerts
6. Use a production ASGI server (Gunicorn + Uvicorn)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Support

For issues or questions:
- Check the API documentation at http://localhost:8000/api/docs
- Review the logs in the terminal
- Ensure all dependencies are installed correctly
