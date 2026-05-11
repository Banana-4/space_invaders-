from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass
    @abstractmethod
    def handle_input(self):
        pass
    @abstractmethod
    def draw(self):
        pass
