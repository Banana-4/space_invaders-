from enum import Enum
from typing import List


class EventID(Enum):
    QUIT_GAME = 1
    MENU_STATE = 2
    PLAY_STATE = 3
    PAUSE_STATE = 4
    HIGHSCORE_STATE = 5
    LOSE = 6
    WIN = 7
    SHOT_FIRED = 8
    FLEET_COLLISION = 9
    HIT = 10
    BORDER_COLLISON = 11
    RESUME = 12
    RESTART = 13


class Event:
    def __init__(self, id: EventID, data: List) -> None:
        self.id = id
        self.data = data


class EventSystem:
    def __init__(self) -> None:
        self.listeners = {}
        self.events = []
        self.add_list = []
        self.remove_list = []

    def register(self, listener, events_id: list[EventID]) -> None:
        self.add_list.append((listener, events_id))

    def add_listeners(self) -> None:
        while self.add_list:
            listener, events_id = self.add_list.pop()
            if listener not in self.listeners:
                self.listeners[listener] = set()
            for id in events_id:
                self.listeners[listener].add(id)

    def unregister(self, listener):
        self.remove_list.append(listener)

    def remove_listener(self):
        while self.remove_list:
            listener = self.remove_list.pop()
            if listener in self.listeners:
                del self.listeners[listener]

    def emitte(self, event: Event) -> None:
        self.remove_listener()
        self.add_listeners()
        self.events.append(event)

    def notify(self) -> None:
        for event in self.events:
            for listener, ids in self.listeners.items():
                if event.id in ids:
                    listener.notify(event)
        self.events = []


events_proxy = EventSystem()
