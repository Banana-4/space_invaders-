from enum import Enum
from typing import List


class EventID(Enum):
    QUIT_GAME = 1
    MENU_STATE = 2
    PLAY_STATE = 3
    PAUSE_STATE = 4
    HIGHSCHORE_STATE = 5
    LOSE = 6
    WIN = 7
    SHOT_FIRED = 8
    FLEET_COLLISION = 9


class Event:
    def __init__(self, id: EventID, data: List) -> None:
        self.id = id
        self.data = data


class EventDispathchare:
    def __init__(self) -> None:
        self.listeners = {}
        self.events = []

    def register(self, listener, events_id: list[EventID]) -> None:
        for id in events_id:
            if id not in self.listeners:
                self.listeners[id] = [listener]
            else:
                self.listeners[id].append(listener)

    def emitte(self, event: Event) -> None:
        self.events.append(event)

    def notifie(self) -> None:
        for event in self.events:
            for listener in self.listeners[event.id]:
                listener.notify(event)
