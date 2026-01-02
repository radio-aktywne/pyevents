from abc import ABC, abstractmethod


class Event(ABC):
    """Base class for events."""

    @abstractmethod
    async def wait(self) -> None:
        """Wait for the event to happen."""

    @abstractmethod
    async def notify(self) -> None:
        """Notify that the event has happened."""
