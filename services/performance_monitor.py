"""
services/performance_monitor.py
Real-time Performance Monitoring System for DENSO888
เฮียตอมจัดหั้ย!!! 🚀
"""

import time
import psutil
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from collections import deque
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Performance metric data structure"""

    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemSnapshot:
    """System performance snapshot"""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    active_connections: int
    import_speed_rows_per_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": self.memory_used_mb,
            "memory_available_mb": self.memory_available_mb,
            "disk_io_read_mb": self.disk_io_read_mb,
            "disk_io_write_mb": self.disk_io_write_mb,
            "network_sent_mb": self.network_sent_mb,
            "network_recv_mb": self.network_recv_mb,
            "active_connections": self.active_connections,
            "import_speed_rows_per_sec": self.import_speed_rows_per_sec,
        }


class BottleneckDetector:
    """Automatic bottleneck detection system"""

    def __init__(self):
        self.thresholds = {
            "cpu_critical": 90.0,
            "cpu_warning": 70.0,
            "memory_critical": 85.0,
            "memory_warning": 70.0,
            "disk_io_high": 100.0,  # MB/s
            "import_speed_low": 100.0,  # rows/sec
        }

        self.bottleneck_history: deque = deque(maxlen=50)

    def analyze_snapshot(self, snapshot: SystemSnapshot) -> List[Dict[str, Any]]:
        """Analyze system snapshot for bottlenecks"""
        bottlenecks = []

        # CPU Analysis
        if snapshot.cpu_percent >= self.thresholds["cpu_critical"]:
            bottlenecks.append(
                {
                    "type": "cpu",
                    "severity": "critical",
                    "message": f"CPU usage critical: {snapshot.cpu_percent:.1f}%",
                    "recommendation": "Consider reducing batch size or parallel workers",
                    "metric_value": snapshot.cpu_percent,
                }
            )
        elif snapshot.cpu_percent >= self.thresholds["cpu_warning"]:
            bottlenecks.append(
                {
                    "type": "cpu",
                    "severity": "warning",
                    "message": f"High CPU usage: {snapshot.cpu_percent:.1f}%",
                    "recommendation": "Monitor CPU-intensive operations",
                    "metric_value": snapshot.cpu_percent,
                }
            )

        # Memory Analysis
        if snapshot.memory_percent >= self.thresholds["memory_critical"]:
            bottlenecks.append(
                {
                    "type": "memory",
                    "severity": "critical",
                    "message": f"Memory usage critical: {snapshot.memory_percent:.1f}%",
                    "recommendation": "Reduce chunk size or restart application",
                    "metric_value": snapshot.memory_percent,
                }
            )
        elif snapshot.memory_percent >= self.thresholds["memory_warning"]:
            bottlenecks.append(
                {
                    "type": "memory",
                    "severity": "warning",
                    "message": f"High memory usage: {snapshot.memory_percent:.1f}%",
                    "recommendation": "Monitor large file processing",
                    "metric_value": snapshot.memory_percent,
                }
            )

        # Import Speed Analysis
        if (
            snapshot.import_speed_rows_per_sec > 0
            and snapshot.import_speed_rows_per_sec < self.thresholds["import_speed_low"]
        ):
            bottlenecks.append(
                {
                    "type": "import_performance",
                    "severity": "warning",
                    "message": f"Slow import speed: {snapshot.import_speed_rows_per_sec:.0f} rows/sec",
                    "recommendation": "Check database performance and network connectivity",
                    "metric_value": snapshot.import_speed_rows_per_sec,
                }
            )

        # Disk I/O Analysis
        total_disk_io = snapshot.disk_io_read_mb + snapshot.disk_io_write_mb
        if total_disk_io > self.thresholds["disk_io_high"]:
            bottlenecks.append(
                {
                    "type": "disk_io",
                    "severity": "warning",
                    "message": f"High disk I/O: {total_disk_io:.1f} MB/s",
                    "recommendation": "Consider SSD upgrade or optimize file operations",
                    "metric_value": total_disk_io,
                }
            )

        # Store bottleneck history
        if bottlenecks:
            self.bottleneck_history.append(
                {"timestamp": snapshot.timestamp, "bottlenecks": bottlenecks}
            )

        return bottlenecks

    def get_bottleneck_trends(self) -> Dict[str, Any]:
        """Get bottleneck trends analysis"""
        if not self.bottleneck_history:
            return {"no_data": True}

        # Count bottleneck types
        type_counts = {}
        severity_counts = {"critical": 0, "warning": 0}

        for record in self.bottleneck_history:
            for bottleneck in record["bottlenecks"]:
                b_type = bottleneck["type"]
                severity = bottleneck["severity"]

                type_counts[b_type] = type_counts.get(b_type, 0) + 1
                severity_counts[severity] += 1

        return {
            "total_incidents": len(self.bottleneck_history),
            "type_distribution": type_counts,
            "severity_distribution": severity_counts,
            "most_common_bottleneck": (
                max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
            ),
            "recent_incidents": list(self.bottleneck_history)[-5:],  # Last 5 incidents
        }


class PerformanceMonitor:
    """Real-time performance monitoring system"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Data storage
        self.snapshots: deque = deque(maxlen=1000)  # Keep last 1000 snapshots
        self.metrics_history: Dict[str, deque] = {}

        # Components
        self.bottleneck_detector = BottleneckDetector()

        # Callbacks
        self.alert_callbacks: List[Callable] = []
        self.data_callbacks: List[Callable] = []

        # Performance tracking
        self.import_start_time: Optional[datetime] = None
        self.import_rows_processed = 0

        # Baseline system info
        self.baseline_snapshot = self._capture_system_snapshot()

        # Stats directory
        self.stats_dir = Path("logs/performance")
        self.stats_dir.mkdir(exist_ok=True)

    def _get_default_config(self) -> Dict[str, Any]:
        """Default monitoring configuration"""
        return {
            "sampling_interval": 2.0,  # seconds
            "enable_disk_io": True,
            "enable_network_io": True,
            "enable_memory_tracking": True,
            "enable_bottleneck_detection": True,
            "save_to_file": True,
            "alert_thresholds": {
                "cpu_critical": 90.0,
                "memory_critical": 85.0,
                "import_speed_critical": 50.0,
            },
        }

    def start_monitoring(self):
        """Start performance monitoring"""
        if self.is_monitoring:
            logger.warning("Performance monitoring already active")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitor_thread.start()

        logger.info("🚀 Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        # Save final stats
        if self.config["save_to_file"]:
            self._save_performance_stats()

        logger.info("📊 Performance monitoring stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        prev_disk_io = None
        prev_network_io = None

        while self.is_monitoring:
            try:
                # Capture system snapshot
                snapshot = self._capture_system_snapshot()

                # Calculate rates (per second values)
                if prev_disk_io:
                    time_diff = (
                        snapshot.timestamp - prev_disk_io["timestamp"]
                    ).total_seconds()
                    if time_diff > 0:
                        disk_read_rate = (
                            snapshot.disk_io_read_mb - prev_disk_io["read"]
                        ) / time_diff
                        disk_write_rate = (
                            snapshot.disk_io_write_mb - prev_disk_io["write"]
                        ) / time_diff
                        snapshot.disk_io_read_mb = max(0, disk_read_rate)
                        snapshot.disk_io_write_mb = max(0, disk_write_rate)

                if prev_network_io:
                    time_diff = (
                        snapshot.timestamp - prev_network_io["timestamp"]
                    ).total_seconds()
                    if time_diff > 0:
                        net_sent_rate = (
                            snapshot.network_sent_mb - prev_network_io["sent"]
                        ) / time_diff
                        net_recv_rate = (
                            snapshot.network_recv_mb - prev_network_io["recv"]
                        ) / time_diff
                        snapshot.network_sent_mb = max(0, net_sent_rate)
                        snapshot.network_recv_mb = max(0, net_recv_rate)

                # Calculate import speed
                snapshot.import_speed_rows_per_sec = self._calculate_import_speed()

                # Store snapshot
                self.snapshots.append(snapshot)

                # Update metrics history
                self._update_metrics_history(snapshot)

                # Detect bottlenecks
                if self.config["enable_bottleneck_detection"]:
                    bottlenecks = self.bottleneck_detector.analyze_snapshot(snapshot)
                    if bottlenecks:
                        self._trigger_alerts(bottlenecks)

                # Notify data callbacks
                for callback in self.data_callbacks:
                    try:
                        callback(snapshot)
                    except Exception as e:
                        logger.error(f"Data callback error: {e}")

                # Store previous values for rate calculation
                prev_disk_io = {
                    "timestamp": snapshot.timestamp,
                    "read": snapshot.disk_io_read_mb,
                    "write": snapshot.disk_io_write_mb,
                }
                prev_network_io = {
                    "timestamp": snapshot.timestamp,
                    "sent": snapshot.network_sent_mb,
                    "recv": snapshot.network_recv_mb,
                }

                # Sleep until next sampling
                time.sleep(self.config["sampling_interval"])

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(1)

    def _capture_system_snapshot(self) -> SystemSnapshot:
        """Capture current system performance snapshot"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()

            # Disk I/O
            disk_io = psutil.disk_io_counters()
            disk_read_mb = disk_io.read_bytes / (1024 * 1024) if disk_io else 0
            disk_write_mb = disk_io.write_bytes / (1024 * 1024) if disk_io else 0

            # Network I/O
            network_io = psutil.net_io_counters()
            network_sent_mb = network_io.bytes_sent / (1024 * 1024) if network_io else 0
            network_recv_mb = network_io.bytes_recv / (1024 * 1024) if network_io else 0

            # Active connections (placeholder - would integrate with connection pool)
            active_connections = (
                len(psutil.net_connections())
                if hasattr(psutil, "net_connections")
                else 0
            )

            return SystemSnapshot(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_io_read_mb=disk_read_mb,
                disk_io_write_mb=disk_write_mb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb,
                active_connections=active_connections,
            )

        except Exception as e:
            logger.error(f"Failed to capture system snapshot: {e}")
            return SystemSnapshot(
                timestamp=datetime.now(),
                cpu_percent=0,
                memory_percent=0,
                memory_used_mb=0,
                memory_available_mb=0,
                disk_io_read_mb=0,
                disk_io_write_mb=0,
                network_sent_mb=0,
                network_recv_mb=0,
                active_connections=0,
            )

    def _calculate_import_speed(self) -> float:
        """Calculate current import speed in rows per second"""
        if not self.import_start_time or self.import_rows_processed == 0:
            return 0.0

        elapsed_time = (datetime.now() - self.import_start_time).total_seconds()
        if elapsed_time <= 0:
            return 0.0

        return self.import_rows_processed / elapsed_time

    def _update_metrics_history(self, snapshot: SystemSnapshot):
        """Update metrics history for trend analysis"""
        metrics = {
            "cpu_percent": snapshot.cpu_percent,
            "memory_percent": snapshot.memory_percent,
            "disk_io_total": snapshot.disk_io_read_mb + snapshot.disk_io_write_mb,
            "network_io_total": snapshot.network_sent_mb + snapshot.network_recv_mb,
            "import_speed": snapshot.import_speed_rows_per_sec,
        }

        for metric_name, value in metrics.items():
            if metric_name not in self.metrics_history:
                self.metrics_history[metric_name] = deque(maxlen=500)
            self.metrics_history[metric_name].append(
                PerformanceMetric(
                    timestamp=snapshot.timestamp,
                    metric_name=metric_name,
                    value=value,
                    unit=self._get_metric_unit(metric_name),
                )
            )

    def _get_metric_unit(self, metric_name: str) -> str:
        """Get unit for metric"""
        units = {
            "cpu_percent": "%",
            "memory_percent": "%",
            "disk_io_total": "MB/s",
            "network_io_total": "MB/s",
            "import_speed": "rows/sec",
        }
        return units.get(metric_name, "")

    def _trigger_alerts(self, bottlenecks: List[Dict[str, Any]]):
        """Trigger alerts for detected bottlenecks"""
        for callback in self.alert_callbacks:
            try:
                callback(bottlenecks)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")

    def _save_performance_stats(self):
        """Save performance statistics to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stats_file = self.stats_dir / f"performance_stats_{timestamp}.json"

            # Prepare data
            stats_data = {
                "session_info": {
                    "start_time": self.baseline_snapshot.timestamp.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "total_snapshots": len(self.snapshots),
                    "config": self.config,
                },
                "performance_summary": self.get_performance_summary(),
                "bottleneck_analysis": self.bottleneck_detector.get_bottleneck_trends(),
                "recent_snapshots": [s.to_dict() for s in list(self.snapshots)[-50:]],
            }

            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False)

            logger.info(f"📈 Performance stats saved to {stats_file}")

        except Exception as e:
            logger.error(f"Failed to save performance stats: {e}")

    # Public API Methods

    def start_import_tracking(self):
        """Start tracking import performance"""
        self.import_start_time = datetime.now()
        self.import_rows_processed = 0
        logger.info("📊 Import performance tracking started")

    def update_import_progress(self, rows_processed: int):
        """Update import progress"""
        self.import_rows_processed = rows_processed

    def stop_import_tracking(self):
        """Stop tracking import performance"""
        final_speed = self._calculate_import_speed()
        self.import_start_time = None
        self.import_rows_processed = 0
        logger.info(
            f"📊 Import tracking stopped. Final speed: {final_speed:.0f} rows/sec"
        )
        return final_speed

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        if not self.snapshots:
            return {"no_data": True}

        latest = self.snapshots[-1]
        return {
            "timestamp": latest.timestamp.isoformat(),
            "cpu_percent": latest.cpu_percent,
            "memory_percent": latest.memory_percent,
            "memory_used_mb": latest.memory_used_mb,
            "import_speed_rows_per_sec": latest.import_speed_rows_per_sec,
            "disk_io_rate_mb_per_sec": latest.disk_io_read_mb + latest.disk_io_write_mb,
            "network_io_rate_mb_per_sec": latest.network_sent_mb
            + latest.network_recv_mb,
            "active_connections": latest.active_connections,
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        if not self.snapshots:
            return {"no_data": True}

        snapshots_list = list(self.snapshots)

        # Calculate averages
        avg_cpu = sum(s.cpu_percent for s in snapshots_list) / len(snapshots_list)
        avg_memory = sum(s.memory_percent for s in snapshots_list) / len(snapshots_list)
        avg_import_speed = sum(
            s.import_speed_rows_per_sec
            for s in snapshots_list
            if s.import_speed_rows_per_sec > 0
        )
        avg_import_speed = avg_import_speed / max(
            1, len([s for s in snapshots_list if s.import_speed_rows_per_sec > 0])
        )

        # Find peaks
        max_cpu = max(s.cpu_percent for s in snapshots_list)
        max_memory = max(s.memory_percent for s in snapshots_list)
        max_import_speed = max(s.import_speed_rows_per_sec for s in snapshots_list)

        return {
            "monitoring_duration_minutes": (
                snapshots_list[-1].timestamp - snapshots_list[0].timestamp
            ).total_seconds()
            / 60,
            "total_snapshots": len(snapshots_list),
            "averages": {
                "cpu_percent": round(avg_cpu, 1),
                "memory_percent": round(avg_memory, 1),
                "import_speed_rows_per_sec": round(avg_import_speed, 1),
            },
            "peaks": {
                "max_cpu_percent": round(max_cpu, 1),
                "max_memory_percent": round(max_memory, 1),
                "max_import_speed_rows_per_sec": round(max_import_speed, 1),
            },
            "system_baseline": {
                "cpu_baseline": round(self.baseline_snapshot.cpu_percent, 1),
                "memory_baseline": round(self.baseline_snapshot.memory_percent, 1),
            },
        }

    def get_bottleneck_report(self) -> Dict[str, Any]:
        """Get comprehensive bottleneck analysis report"""
        return self.bottleneck_detector.get_bottleneck_trends()

    def register_alert_callback(self, callback: Callable):
        """Register callback for performance alerts"""
        self.alert_callbacks.append(callback)

    def register_data_callback(self, callback: Callable):
        """Register callback for performance data updates"""
        self.data_callbacks.append(callback)

    def get_realtime_data(self, last_n_snapshots: int = 60) -> List[Dict[str, Any]]:
        """Get real-time performance data for dashboard"""
        recent_snapshots = list(self.snapshots)[-last_n_snapshots:]
        return [snapshot.to_dict() for snapshot in recent_snapshots]

    def cleanup(self):
        """Cleanup monitoring resources"""
        self.stop_monitoring()
        self.alert_callbacks.clear()
        self.data_callbacks.clear()
        logger.info("🧹 Performance monitor cleanup completed")
