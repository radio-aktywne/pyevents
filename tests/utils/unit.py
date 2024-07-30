import asyncio
from abc import ABC, abstractmethod

import pytest

from pyevents.base import Event


class EventLifespan(ABC):
    """Base class for managing the lifespan of a event."""

    async def __aenter__(self) -> Event:
        return await self.enter()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.exit()

    @abstractmethod
    async def enter(self) -> Event:
        """Enter the lifespan of the event."""

        pass

    @abstractmethod
    async def exit(self) -> None:
        """Exit the lifespan of the event."""

        pass


class EventLifespanBuilder(ABC):
    """Base class for building a event lifespan."""

    @abstractmethod
    async def build(self) -> EventLifespan:
        """Build a event lifespan."""

        pass


class BaseEventTest(ABC):
    """Base class for testing a event."""

    @pytest.fixture()
    @abstractmethod
    def builder(self) -> EventLifespanBuilder:
        """Return a builder for a event lifespan."""

        pass

    @pytest.mark.asyncio(scope="session")
    async def test_wait_notify(self, builder: EventLifespanBuilder) -> None:
        """Test that waiting and notifying works."""

        waiter_allowed_to_wait = asyncio.Event()
        waiter_tried = asyncio.Event()
        waiter_finished = asyncio.Event()
        notifier_allowed_to_notify = asyncio.Event()
        notifier_finished = asyncio.Event()

        async def wait() -> None:
            await waiter_allowed_to_wait.wait()
            waiter_tried.set()
            await event.wait()
            waiter_finished.set()

        async def notify() -> None:
            await notifier_allowed_to_notify.wait()
            await event.notify()
            notifier_finished.set()

        async with await builder.build() as event:
            waiter = asyncio.create_task(wait())
            notifier = asyncio.create_task(notify())

            assert not waiter_finished.is_set()

            waiter_allowed_to_wait.set()
            await waiter_tried.wait()

            assert not waiter_finished.is_set()

            notifier_allowed_to_notify.set()
            await notifier_finished.wait()

            await waiter_finished.wait()

            await waiter
            await notifier
