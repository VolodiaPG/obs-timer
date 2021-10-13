""" A simple event bus """
import asyncio
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable, Coroutine, Type, TypeVar


class Event(ABC):
    """Base class demonstrating what type is an event made of"""


Template = TypeVar("Template", bound=Event)


class EventBus(ABC):
    """The contract of what an EventBus posses"""

    @abstractmethod
    def emit(self, event: Event) -> None:
        """Emits an event on the bus

        Args:
            event: The event instance to use
        """

    @abstractmethod
    def add_listener(
        self,
        event: Type[Template],
        func: Callable[[Template], Coroutine[None, None, None]],
    ) -> None:
        """Adds a listener to a particular type of event

        Args:
            event: The type of the event to catch
            func: The async callback that will process the event
        """

    @abstractmethod
    def remove_listener(
        self,
        event: Type[Template],
        func: Callable[[Template], Coroutine[None, None, None]],
    ) -> None:
        """Removes a listener from a particular event type

        Args:
            event: The type of the event remove the callback from
            func: The async callback that was used to process the event
        """


class AsyncEventBus(EventBus):
    """A simple event bus class."""

    # Memory optimization for faster access to attributes and space savings
    __slots__ = ["_events"]

    def __init__(self) -> None:
        """Creates new AsyncEventBus object."""

        self._events: dict[
            Type[Event], set[Callable[[Template], Coroutine[None, None, None]]]
        ] = defaultdict(set)

    def emit(self, event: Event) -> None:
        for func in self._events[type(event)]:
            func(event)

    def add_listener(
        self,
        event: Type[Template],
        func: Callable[[Template], Coroutine[None, None, None]],
    ) -> None:
        self._events[event].add(func)

    def remove_listener(
        self,
        event: Type[Template],
        func: Callable[[Template], Coroutine[None, None, None]],
    ) -> None:
        self._events[event].remove(func)

        if len(self._events[event]) == 0:
            del self._events[event]