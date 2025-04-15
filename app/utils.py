import requests
import json
from datetime import datetime
from app.models import db, SystemMetric

def fetch_netdata_metrics(host_ip):
    """
    Fetch metrics from a specific host's Netdata instance
    """
    try:
        # For CPU data
        cpu_response = requests.get(f"http://{host_ip}:19999/api/v1/data?chart=system.cpu&points=1", timeout=5)
        cpu_data = cpu_response.json()
        
        # For memory data
        memory_response = requests.get(f"http://{host_ip}:19999/api/v1/data?chart=system.ram&points=1", timeout=5)
        memory_data = memory_response.json()
        
        # For disk data (root filesystem)
        disk_response = requests.get(f"http://{host_ip}:19999/api/v1/data?chart=disk_space._&points=1", timeout=5)
        disk_data = disk_response.json()
        
        # For network data (aggregate of all interfaces)
        network_response = requests.get(f"http://{host_ip}:19999/api/v1/data?chart=system.net&points=1", timeout=5)
        network_data = network_response.json()
        
        # Parse the collected data
        metric = SystemMetric(
            host_ip=host_ip,
            timestamp=datetime.utcnow(),
            is_reachable=True
        )
        
        # CPU metrics - data is typically in percentages
        if 'data' in cpu_data and len(cpu_data['data']) > 0:
            data_point = cpu_data['data'][0]
            metric.cpu_user = data_point[1]  # Index depends on Netdata's format
            metric.cpu_system = data_point[3]
            metric.cpu_idle = data_point[2]
            metric.cpu_iowait = data_point[4]
        
        # Memory metrics - data is typically in bytes
        if 'data' in memory_data and len(memory_data['data']) > 0:
            data_point = memory_data['data'][0]
            metric.memory_total = data_point[1]
            metric.memory_free = data_point[2]
            metric.memory_used = data_point[3]
            metric.memory_cached = data_point[4]
        
        # Disk metrics - data is typically in bytes
        if 'data' in disk_data and len(disk_data['data']) > 0:
            data_point = disk_data['data'][0]
            metric.disk_total = data_point[1]
            metric.disk_used = data_point[2]
            metric.disk_free = data_point[3]
        
        # Network metrics - data is typically in bytes/s
        if 'data' in network_data and len(network_data['data']) > 0:
            data_point = network_data['data'][0]
            metric.network_received_bytes = data_point[1]
            metric.network_sent_bytes = data_point[2]
        
        return metric
    
    except Exception as e:
        # Handle the case where a machine is unreachable
        return SystemMetric(
            host_ip=host_ip,
            timestamp=datetime.utcnow(),
            is_reachable=False,
            error_message=str(e)
        )

def collect_all_metrics(cluster_ips):
    """
    Collect metrics from all machines in the cluster
    """
    metrics = []
    for ip in cluster_ips:
        metric = fetch_netdata_metrics(ip)
        db.session.add(metric)
        metrics.append(metric)
    
    db.session.commit()
    return metrics
