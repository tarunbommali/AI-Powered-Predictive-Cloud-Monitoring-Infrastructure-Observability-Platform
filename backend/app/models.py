"""
SQLAlchemy database models
"""
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    instances = relationship("Instance", back_populates="owner")
    alert_configs = relationship("AlertConfig", back_populates="user")


class Instance(Base):
    """EC2 Instance model"""
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instance_id = Column(String, unique=True, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, default=9100)
    region = Column(String)
    instance_type = Column(String)
    status = Column(String, default="active")
    is_monitored = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="instances")
    alerts = relationship("Alert", back_populates="instance")
    metrics_snapshots = relationship("MetricsSnapshot", back_populates="instance")


class Alert(Base):
    """Alert history model"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("instances.id"))
    alert_type = Column(String)  # cpu, memory, disk, network
    metric_name = Column(String)
    threshold_value = Column(Float)
    current_value = Column(Float)
    severity = Column(String)  # warning, critical
    message = Column(String)
    status = Column(String, default="active")  # active, resolved, acknowledged
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    instance = relationship("Instance", back_populates="alerts")


class AlertConfig(Base):
    """Alert configuration model"""
    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String)  # cpu, memory, disk
    threshold = Column(Float)
    duration_minutes = Column(Integer, default=5)
    enabled = Column(Boolean, default=True)
    notification_email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="alert_configs")


# class MetricsSnapshot(Base):
#     """Store periodic snapshots of metrics for historical analysis"""
#     __tablename__ = "metrics_snapshots"

#     id = Column(Integer, primary_key=True, index=True)
#     instance_id = Column(Integer, ForeignKey("instances.id"))
#     timestamp = Column(DateTime(timezone=True), server_default=func.now())
#     cpu_usage = Column(Float)
#     memory_usage = Column(Float)
#     disk_usage = Column(Float)
#     network_rx = Column(Float)
#     network_tx = Column(Float)
#     load_1min = Column(Float)
#     load_5min = Column(Float)
#     load_15min = Column(Float)


class MetricsSnapshot(Base):
    """
    Metrics snapshot for ML training - ADDED FOR ML FEATURES
    Stores historical metrics data for machine learning model training
    """
    __tablename__ = "metrics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("instances.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_rx = Column(Float)
    network_tx = Column(Float)
    network_rx_errors = Column(Float, default=0)
    network_tx_errors = Column(Float, default=0)
    disk_read_bytes = Column(Float, default=0)
    disk_write_bytes = Column(Float, default=0)
    load_1min = Column(Float)
    load_5min = Column(Float)
    load_15min = Column(Float)

    instance = relationship("Instance", back_populates="metrics_snapshots")
