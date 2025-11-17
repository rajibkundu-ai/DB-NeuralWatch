from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.schemas import AGReplicaStatus


@dataclass
class _ReplicaProfile:
    name: str
    role: str
    base_latency: float
    sync_state: str


class AGMonitor:
    """Generates lightweight Availability Group replica health snapshots."""

    def __init__(self) -> None:
        self._replicas: List[_ReplicaProfile] = [
            _ReplicaProfile(name="SQL01-PRIMARY", role="Primary", base_latency=3.0, sync_state="Synchronized"),
            _ReplicaProfile(name="SQL02-SECONDARY", role="Secondary", base_latency=6.0, sync_state="Synchronized"),
            _ReplicaProfile(name="SQL03-DR", role="Async Secondary", base_latency=12.0, sync_state="Synchronizing"),
        ]

    def current_status(self) -> List[AGReplicaStatus]:
        minute = datetime.utcnow().minute
        drift = (minute % 6) - 3  # [-3, 2]
        status: List[AGReplicaStatus] = []
        for index, replica in enumerate(self._replicas):
            latency = max(1.0, replica.base_latency + (index * 1.5) + drift)
            log_queue = max(0.2, 0.9 + (index * 0.4) + drift * 0.1)
            redo_queue = max(0.1, 0.5 + (index * 0.3) + drift * 0.05)
            health = "healthy"
            sync_state = replica.sync_state
            if latency > 15:
                health = "critical"
                sync_state = "Re-synchronizing"
            elif latency > 8:
                health = "watch"
                sync_state = "Synchronizing"
            status.append(
                AGReplicaStatus(
                    name=replica.name,
                    role=replica.role,
                    health=health,
                    synchronization_state=sync_state,
                    log_send_queue_mb=round(log_queue, 1),
                    redo_queue_mb=round(redo_queue, 1),
                    latency_ms=round(latency, 1),
                )
            )
        return status
