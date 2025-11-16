from __future__ import annotations

import uuid
from typing import List

from app.core.config import get_settings
from app.models.schemas import Alert, MetricSample
from app.storage import repository


class AlertManager:
    def __init__(self) -> None:
        self.settings = get_settings()

    def evaluate(self, sample: MetricSample) -> List[Alert]:
        alerts: List[Alert] = []
        if sample.cpu_percent >= self.settings.alert_cpu_threshold:
            alerts.append(self._build_alert("CPU utilization exceeded threshold", "critical"))
        if sample.memory_percent >= self.settings.alert_memory_threshold:
            alerts.append(self._build_alert("Memory pressure detected", "warning"))
        if sample.disk_io >= self.settings.alert_disk_io_threshold:
            alerts.append(self._build_alert("High disk I/O detected", "warning"))
        if sample.deadlocks > 0:
            alerts.append(self._build_alert("Deadlocks observed", "critical"))
        if sample.blocking_sessions > 3:
            alerts.append(self._build_alert("Blocking sessions increasing", "warning"))
        for alert in alerts:
            repository.save_alert(alert)
        return alerts

    def _build_alert(self, message: str, severity: str) -> Alert:
        return Alert(id=str(uuid.uuid4()), message=message, severity=severity)


alert_manager = AlertManager()
