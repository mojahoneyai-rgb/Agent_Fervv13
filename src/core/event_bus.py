"""
Event Bus System
Handles decoupling of components via publish/subscribe pattern.
"""
from typing import Callable, Any, Dict, List

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def publish(self, event_name: str, data: Any = None):
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error handling event {event_name}: {e}")

# Global instance for app-wide events
global_event_bus = EventBus()
