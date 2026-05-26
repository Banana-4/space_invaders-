from abc import ABC, abstractmethod

import pygame


class State(ABC):
    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def handle_input(self) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
