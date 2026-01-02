from typing import override

import pytest

from pyevents.asyncio import AsyncioEvent
from tests.utils.unit import BaseEventTest, EventLifespan, EventLifespanBuilder


class AsyncioEventLifespan(EventLifespan):
    """Lifespan for AsyncioEvent."""

    def __init__(self, event: AsyncioEvent) -> None:
        self._event = event

    @override
    async def enter(self) -> AsyncioEvent:
        return self._event

    @override
    async def exit(self) -> None:
        return None


class AsyncioEventLifespanBuilder(EventLifespanBuilder):
    """Builder for AsyncioEventLifespan."""

    @override
    async def build(self) -> AsyncioEventLifespan:
        return AsyncioEventLifespan(AsyncioEvent())


class TestAsyncioEvent(BaseEventTest):
    """Tests for AsyncioEvent."""

    @pytest.fixture
    @override
    def builder(self) -> AsyncioEventLifespanBuilder:
        return AsyncioEventLifespanBuilder()
