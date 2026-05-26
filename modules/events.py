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
        if listener not in self.listeners:
            self.listeners[listener] = set()
        for id in events_id:
            self.listeners[listener].add(id)

    def emitte(self, event: Event) -> None:
        self.events.append(event)

    def notify(self) -> None:
        while len(self.events) > 0:
            event = self.events.pop()
            for listener, ids in self.listeners.items():
                if event.id in ids:
                    listener.notify(event)
                    if event.id in (
                        EventID.PLAY_STATE,
                        EventID.HIGHSCHORE_STATE,
                        EventID.MENU_STATE,
                    ):
                        self.events = []
                        return


events_proxy = EventDispathchare()
