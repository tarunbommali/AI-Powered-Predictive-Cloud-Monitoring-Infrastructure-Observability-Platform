"""
ML-Enhanced API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app import models, auth
from app.ml_models.anomaly_detector import anomaly_detector
from app.ml_models.cpu_predictor import cpu_predictor
from app.ml_models.memory_predictor import memory_predictor
from app.ml_models.health_scorer import health_scorer
from app.ml_models.failure_predictor import failure_predictor
from app.ml_models.root_cause_analyzer import root_cause_analyzer
from app.ml_models.capacity_planner import capacity_planner
from app.services.prometheus import prometheus_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.post("/anomaly/train/{instance_id}")
async def train_anomaly_detector(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Train anomaly detection model for an instance"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get historical metrics (last 7 days)
    historical_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    if len(historical_data) < 100:
        raise HTTPException(status_code=400, detail="Insufficient historical data (need at least 100 samples)")
    
    # Prepare training data
    training_data = [{
        'cpu_usage': m.cpu_usage,
        'memory_usage': m.memory_usage,
        'disk_usage': m.disk_usage,
        'network_rx': m.network_rx,
        'network_tx': m.network_tx,
        'load_1min': m.load_1min,
        'load_5min': m.load_5min,
        'load_15min': m.load_15min
    } for m in historical_data]
    
    # Train model
    result = anomaly_detector.train(training_data)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/anomaly/detect/{instance_id}")
async def detect_anomaly(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Detect anomalies in current metrics"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get current metrics from Prometheus
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    disk_metrics = prometheus_client.get_disk_usage(target)
    network_metrics = prometheus_client.get_network_usage(target)
    load_avg = prometheus_client.get_load_average(target)
    
    current_metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0),
        'disk_usage': disk_metrics.get('usage_percent', 0),
        'network_rx': network_metrics.get('rx_bytes', 0),
        'network_tx': network_metrics.get('tx_bytes', 0),
        'load_1min': load_avg.get('load_1min', 0),
        'load_5min': load_avg.get('load_5min', 0),
        'load_15min': load_avg.get('load_15min', 0)
    }
    
    # Detect anomaly
    result = anomaly_detector.detect(current_metrics)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name,
        'current_metrics': current_metrics
    }


@router.post("/cpu/train/{instance_id}")
async def train_cpu_predictor(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Train CPU prediction model"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get historical data
    historical_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    if len(historical_data) < 100:
        raise HTTPException(status_code=400, detail="Insufficient data")
    
    training_data = [{
        'timestamp': m.timestamp,
        'cpu_usage': m.cpu_usage
    } for m in historical_data]
    
    result = cpu_predictor.train(training_data)
    return result


@router.get("/cpu/predict/{instance_id}")
async def predict_cpu(
    instance_id: str,
    minutes: int = 30,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Predict CPU usage for next N minutes"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    predictions = cpu_predictor.predict(minutes_ahead=minutes)
    
    return {
        **predictions,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.post("/memory/train/{instance_id}")
async def train_memory_predictor(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Train memory prediction model"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    historical_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    if len(historical_data) < 100:
        raise HTTPException(status_code=400, detail="Insufficient data")
    
    training_data = [{
        'timestamp': m.timestamp,
        'memory_usage': m.memory_usage
    } for m in historical_data]
    
    result = memory_predictor.train(training_data)
    return result


@router.get("/memory/predict/{instance_id}")
async def predict_memory(
    instance_id: str,
    minutes: int = 30,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Predict memory usage"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    predictions = memory_predictor.predict(minutes_ahead=minutes)
    
    return {
        **predictions,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/memory/leak-detection/{instance_id}")
async def detect_memory_leak(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Detect memory leaks"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get recent data (last 24 hours)
    historical_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    if len(historical_data) < 10:
        raise HTTPException(status_code=400, detail="Insufficient data")
    
    data = [{'timestamp': m.timestamp, 'memory_usage': m.memory_usage} for m in historical_data]
    result = memory_predictor.detect_memory_leak(data)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/health-score/{instance_id}")
async def get_health_score(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Get instance health score"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get current metrics
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    disk_metrics = prometheus_client.get_disk_usage(target)
    network_metrics = prometheus_client.get_network_usage(target)
    load_avg = prometheus_client.get_load_average(target)
    
    metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0),
        'disk_usage': disk_metrics.get('usage_percent', 0),
        'network_rx_errors': network_metrics.get('rx_errors', 0),
        'network_tx_errors': network_metrics.get('tx_errors', 0),
        'load_1min': load_avg.get('load_1min', 0),
        'cpu_count': 4  # You can get this from node_exporter
    }
    
    # Check for anomalies
    anomaly_score = anomaly_detector.detect(metrics)
    
    # Calculate health score
    health_data = health_scorer.calculate_health_score(metrics, anomaly_score)
    
    return {
        **health_data,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/failure/predict/{instance_id}")
async def predict_failure(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Predict system failure"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get current metrics
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    disk_metrics = prometheus_client.get_disk_usage(target)
    network_metrics = prometheus_client.get_network_usage(target)
    load_avg = prometheus_client.get_load_average(target)
    
    current_metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0),
        'disk_usage': disk_metrics.get('usage_percent', 0),
        'load_1min': load_avg.get('load_1min', 0),
        'load_5min': load_avg.get('load_5min', 0),
        'network_rx_errors': network_metrics.get('rx_errors', 0),
        'network_tx_errors': network_metrics.get('tx_errors', 0)
    }
    
    # Get recent metrics
    recent_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(minutes=15)
    ).order_by(models.MetricsSnapshot.timestamp.desc()).limit(5).all()
    
    recent_metrics = [{
        'cpu_usage': m.cpu_usage,
        'memory_usage': m.memory_usage,
        'disk_usage': m.disk_usage
    } for m in recent_data] if recent_data else None
    
    result = failure_predictor.predict_failure(current_metrics, recent_metrics)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/root-cause/{instance_id}")
async def analyze_root_cause(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Analyze root cause of issues"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get current metrics
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    disk_metrics = prometheus_client.get_disk_usage(target)
    network_metrics = prometheus_client.get_network_usage(target)
    load_avg = prometheus_client.get_load_average(target)
    
    metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0),
        'disk_usage': disk_metrics.get('usage_percent', 0),
        'network_rx_bytes': network_metrics.get('rx_bytes', 0),
        'network_rx_errors': network_metrics.get('rx_errors', 0),
        'network_tx_errors': network_metrics.get('tx_errors', 0),
        'disk_write_bytes': disk_metrics.get('write_bytes', 0),
        'load_1min': load_avg.get('load_1min', 0),
        'load_5min': load_avg.get('load_5min', 0)
    }
    
    result = root_cause_analyzer.analyze(metrics)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/capacity/analyze/{instance_id}")
async def analyze_capacity(
    instance_id: str,
    forecast_days: int = 14,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Analyze capacity and scaling needs"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get historical data (last 30 days)
    historical_data = db.query(models.MetricsSnapshot).filter(
        models.MetricsSnapshot.instance_id == instance.id,
        models.MetricsSnapshot.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    if len(historical_data) < 100:
        raise HTTPException(status_code=400, detail="Insufficient historical data")
    
    data = [{
        'cpu_usage': m.cpu_usage,
        'memory_usage': m.memory_usage
    } for m in historical_data]
    
    result = capacity_planner.analyze_capacity(data, forecast_days)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/autoscale/recommend/{instance_id}")
async def get_autoscale_recommendation(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Get auto-scaling recommendations"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get current metrics
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    
    current_metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0)
    }
    
    result = capacity_planner.get_autoscaling_recommendation(current_metrics)
    
    return {
        **result,
        'instance_id': instance.instance_id,
        'instance_name': instance.name
    }


@router.get("/dashboard/ml-summary/{instance_id}")
async def get_ml_dashboard_summary(
    instance_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_optional_current_user)
):
    """Get comprehensive ML analysis for dashboard"""
    if instance_id.isdigit():
        instance = db.query(models.Instance).filter(models.Instance.id == int(instance_id)).first()
    else:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        instance = db.query(models.Instance).filter(models.Instance.instance_id == instance_id).first()
        
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Get all ML insights
    target = f"{instance.ip_address}:{instance.port}"
    cpu_usage = prometheus_client.get_cpu_usage(target)
    memory_metrics = prometheus_client.get_memory_usage(target)
    disk_metrics = prometheus_client.get_disk_usage(target)
    network_metrics = prometheus_client.get_network_usage(target)
    load_avg = prometheus_client.get_load_average(target)
    
    metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_metrics.get('usage_percent', 0),
        'disk_usage': disk_metrics.get('usage_percent', 0),
        'network_rx_bytes': network_metrics.get('rx_bytes', 0),
        'network_rx_errors': network_metrics.get('rx_errors', 0),
        'network_tx_errors': network_metrics.get('tx_errors', 0),
        'disk_write_bytes': disk_metrics.get('write_bytes', 0),
        'load_1min': load_avg.get('load_1min', 0),
        'load_5min': load_avg.get('load_5min', 0),
        'cpu_count': 4
    }
    
    # Get all ML insights
    anomaly = anomaly_detector.detect(metrics)
    health = health_scorer.calculate_health_score(metrics, anomaly)
    failure = failure_predictor.predict_failure(metrics)
    root_cause = root_cause_analyzer.analyze(metrics)
    autoscale = capacity_planner.get_autoscaling_recommendation(metrics)
    
    # Try to get predictions
    try:
        cpu_pred = cpu_predictor.predict(minutes_ahead=30)
        memory_pred = memory_predictor.predict(minutes_ahead=30)
    except:
        cpu_pred = {'predictions': []}
        memory_pred = {'predictions': []}
    
    return {
        'instance_id': instance.instance_id,
        'instance_name': instance.name,
        'health_score': health,
        'anomaly_detection': anomaly,
        'failure_prediction': failure,
        'root_cause_analysis': root_cause,
        'autoscale_recommendation': autoscale,
        'cpu_prediction': cpu_pred.get('predictions', [])[:10],
        'memory_prediction': memory_pred.get('predictions', [])[:10],
        'timestamp': datetime.now().isoformat()
    }
