import pytest

from pyevents.asyncio import AsyncioEvent
from tests.utils.unit import BaseEventTest, EventLifespan, EventLifespanBuilder


class AsyncioEventLifespan(EventLifespan):
    def __init__(self, event: AsyncioEvent) -> None:
        self._event = event

    async def enter(self) -> AsyncioEvent:
        return self._event

    async def exit(self) -> None:
        return None


class AsyncioEventLifespanBuilder(EventLifespanBuilder):
    async def build(self) -> AsyncioEventLifespan:
        return AsyncioEventLifespan(AsyncioEvent())


class TestAsyncioEvent(BaseEventTest):
    @pytest.fixture
    def builder(self) -> AsyncioEventLifespanBuilder:
        return AsyncioEventLifespanBuilder()
