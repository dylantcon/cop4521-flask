"""
Database models for the application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication and role management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False, default='User')  # 'Admin' or 'User'

class MetricLogs(db.Model):
    """Model to store metrics logged from machines via Netdata API."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    machine_name = db.Column(db.String(45), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=True)
    memory_usage = db.Column(db.Float, nullable=True)
    disk_usage = db.Column(db.Float, nullable=True)
    network_usage = db.Column(db.Float, nullable=True)

class SystemMetric(db.Model):
    __tablename__ = 'system_metrics'

    id = db.Column(db.Integer, primary_key=True)
    host_ip = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # cpu metrics
    cpu_user = db.Column(db.Float, nullable=True)
    cpu_system = db.Column(db.Float, nullable=True)
    cpu_idle = db.Column(db.Float, nullable=True)
    cpu_iowait = db.Column(db.Float, nullable=True)

    # memory metrics
    memory_total = db.Column(db.Float, nullable=True)
    memory_used = db.Column(db.Float, nullable=True)
    memory_cached = db.Column(db.Float, nullable=True)
    memory_free = db.Column(db.Float, nullable=True)

    # disk metrics
    disk_total = db.Column(db.Float, nullable=True)
    disk_used = db.Column(db.Float, nullable=True)
    disk_free = db.Column(db.Float, nullable=True)

    # network metrics
    network_received_bytes = db.Column(db.Float, nullable=True)
    network_sent_bytes = db.Column(db.Float, nullable=True)

    # system status
    is_reachable = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<SystemMetric {self.host_ip} at {self.timestamp}>'
