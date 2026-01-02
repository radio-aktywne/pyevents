import asyncio
from typing import override

from pyevents.base import Event


class AsyncioEvent(Event):
    """Asyncio event."""

    def __init__(self) -> None:
        self._event = asyncio.Event()

    @override
    async def wait(self) -> None:
        await self._event.wait()

    @override
    async def notify(self) -> None:
        self._event.set()
        self._event.clear()
