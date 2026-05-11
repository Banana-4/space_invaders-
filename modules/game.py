import pygame

class Game:
    def __init__(self, res: tuple[int, int] = (640, 400)) -> None:
        self.caption: str = "Space Invaders"
        self.win: pygame.Surface  = pygame.display.set_mode(res)
        pygame.display.set_caption(self.caption)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.run = True
        self.fps = 60
        self.state = "menu" # should be object this is just a place holder

    def main(self) -> None: # game loop
        dt = 0
        while self.run:
            dt = self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            self.input()
            self.update(dt)
            self.draw()

    def update(self, dt: float) -> None:
        pass

    def input(self) -> None:
        pass

    def draw(self) -> None:
        self.win.fill("#000000")
        pygame.display.flip()
