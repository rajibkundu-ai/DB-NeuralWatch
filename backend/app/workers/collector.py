from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Awaitable, Callable

from app.core.config import get_settings
from app.models.schemas import MetricSample
from app.services.sql_monitor import SQLServerMonitor
from app.services.alerting import alert_manager
from app.storage import repository


class MetricCollector:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.monitor = SQLServerMonitor()
        self._task: asyncio.Task | None = None
        self.subscribers: list[Callable[[MetricSample], Awaitable[None] | None]] = []

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _run(self) -> None:
        while True:
            sample = self.monitor.collect_metrics()
            repository.save_metric(sample)
            alert_manager.evaluate(sample)
            for subscriber in self.subscribers:
                result = subscriber(sample)
                if asyncio.iscoroutine(result):
                    await result
            repository.cleanup_old_metrics()
            await asyncio.sleep(self.settings.metrics_poll_interval)

    def subscribe(self, handler: Callable[[MetricSample], Awaitable[None] | None]) -> None:
        self.subscribers.append(handler)


collector = MetricCollector()
