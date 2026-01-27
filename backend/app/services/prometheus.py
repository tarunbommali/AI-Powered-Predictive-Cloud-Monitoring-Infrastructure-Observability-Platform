"""
Prometheus client for querying metrics
"""
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class PrometheusClient:
    """Client for interacting with Prometheus API"""
    
    def __init__(self, url: str = settings.PROMETHEUS_URL):
        self.url = url.rstrip('/')
        self.api_url = f"{self.url}/api/v1"
    
    def query(self, query: str) -> Dict[str, Any]:
        """Execute instant query"""
        try:
            response = requests.get(
                f"{self.api_url}/query",
                params={"query": query},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Prometheus query error: {e}")
            return {"status": "error", "data": {"result": []}}
    
    def query_range(self, query: str, start: int, end: int, step: str = "15s") -> Dict[str, Any]:
        """Execute range query"""
        try:
            response = requests.get(
                f"{self.api_url}/query_range",
                params={
                    "query": query,
                    "start": start,
                    "end": end,
                    "step": step
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Prometheus range query error: {e}")
            return {"status": "error", "data": {"result": []}}
    
    def get_cpu_usage(self, instance: str) -> float:
        """Get CPU usage percentage"""
        query = f'100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle",instance="{instance}"}}[5m])) * 100)'
        result = self.query(query)
        
        if result.get("status") == "success" and result.get("data", {}).get("result"):
            return float(result["data"]["result"][0]["value"][1])
        return 0.0
    
    def get_cpu_per_core(self, instance: str) -> List[float]:
        """Get CPU usage per core"""
        query = f'100 - (avg by (cpu) (irate(node_cpu_seconds_total{{mode="idle",instance="{instance}"}}[5m])) * 100)'
        result = self.query(query)
        
        cores = []
        if result.get("status") == "success" and result.get("data", {}).get("result"):
            for item in result["data"]["result"]:
                cores.append(float(item["value"][1]))
        return cores
    
    def get_memory_usage(self, instance: str) -> Dict[str, float]:
        """Get memory usage metrics"""
        queries = {
            "total": f'node_memory_MemTotal_bytes{{instance="{instance}"}}',
            "available": f'node_memory_MemAvailable_bytes{{instance="{instance}"}}',
            "used": f'node_memory_MemTotal_bytes{{instance="{instance}"}} - node_memory_MemAvailable_bytes{{instance="{instance}"}}',
            "swap_total": f'node_memory_SwapTotal_bytes{{instance="{instance}"}}',
            "swap_used": f'node_memory_SwapTotal_bytes{{instance="{instance}"}} - node_memory_SwapFree_bytes{{instance="{instance}"}}'
        }
        
        metrics = {}
        for key, query in queries.items():
            result = self.query(query)
            if result.get("status") == "success" and result.get("data", {}).get("result"):
                metrics[key] = float(result["data"]["result"][0]["value"][1])
            else:
                metrics[key] = 0.0
        
        # Calculate usage percentage
        if metrics["total"] > 0:
            metrics["usage_percent"] = (metrics["used"] / metrics["total"]) * 100
        else:
            metrics["usage_percent"] = 0.0
        
        return metrics
    
    def get_disk_usage(self, instance: str, mount_point: str = "/") -> Dict[str, float]:
        """Get disk usage metrics"""
        queries = {
            "total": f'node_filesystem_size_bytes{{instance="{instance}",mountpoint="{mount_point}"}}',
            "available": f'node_filesystem_avail_bytes{{instance="{instance}",mountpoint="{mount_point}"}}',
            "used": f'node_filesystem_size_bytes{{instance="{instance}",mountpoint="{mount_point}"}} - node_filesystem_avail_bytes{{instance="{instance}",mountpoint="{mount_point}"}}',
            "read_bytes": f'rate(node_disk_read_bytes_total{{instance="{instance}"}}[5m])',
            "write_bytes": f'rate(node_disk_written_bytes_total{{instance="{instance}"}}[5m])'
        }
        
        metrics = {}
        for key, query in queries.items():
            result = self.query(query)
            if result.get("status") == "success" and result.get("data", {}).get("result"):
                if result["data"]["result"]:
                    metrics[key] = float(result["data"]["result"][0]["value"][1])
                else:
                    metrics[key] = 0.0
            else:
                metrics[key] = 0.0
        
        # Calculate usage percentage
        if metrics["total"] > 0:
            metrics["usage_percent"] = (metrics["used"] / metrics["total"]) * 100
        else:
            metrics["usage_percent"] = 0.0
        
        return metrics
    
    def get_network_usage(self, instance: str) -> Dict[str, float]:
        """Get network usage metrics"""
        queries = {
            "rx_bytes": f'rate(node_network_receive_bytes_total{{instance="{instance}",device!="lo"}}[5m])',
            "tx_bytes": f'rate(node_network_transmit_bytes_total{{instance="{instance}",device!="lo"}}[5m])',
            "rx_packets": f'rate(node_network_receive_packets_total{{instance="{instance}",device!="lo"}}[5m])',
            "tx_packets": f'rate(node_network_transmit_packets_total{{instance="{instance}",device!="lo"}}[5m])',
            "rx_errors": f'rate(node_network_receive_errs_total{{instance="{instance}",device!="lo"}}[5m])',
            "tx_errors": f'rate(node_network_transmit_errs_total{{instance="{instance}",device!="lo"}}[5m])'
        }
        
        metrics = {}
        for key, query in queries.items():
            result = self.query(query)
            total = 0.0
            if result.get("status") == "success" and result.get("data", {}).get("result"):
                for item in result["data"]["result"]:
                    total += float(item["value"][1])
            metrics[key] = total
        
        return metrics
    
    def get_load_average(self, instance: str) -> Dict[str, float]:
        """Get load average"""
        queries = {
            "load_1min": f'node_load1{{instance="{instance}"}}',
            "load_5min": f'node_load5{{instance="{instance}"}}',
            "load_15min": f'node_load15{{instance="{instance}"}}'
        }
        
        metrics = {}
        for key, query in queries.items():
            result = self.query(query)
            if result.get("status") == "success" and result.get("data", {}).get("result"):
                metrics[key] = float(result["data"]["result"][0]["value"][1])
            else:
                metrics[key] = 0.0
        
        return metrics
    
    def get_uptime(self, instance: str) -> float:
        """Get system uptime in seconds"""
        query = f'node_time_seconds{{instance="{instance}"}} - node_boot_time_seconds{{instance="{instance}"}}'
        result = self.query(query)
        
        if result.get("status") == "success" and result.get("data", {}).get("result"):
            return float(result["data"]["result"][0]["value"][1])
        return 0.0
    
    def check_health(self) -> bool:
        """Check if Prometheus is healthy"""
        try:
            response = requests.get(f"{self.url}/-/healthy", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False


# Global Prometheus client instance
prometheus_client = PrometheusClient()
