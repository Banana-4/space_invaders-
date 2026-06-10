import os
import random

import pygame

from modules.events import Event, EventID, events_proxy


class Entity:
    def __init__(
        self, sprite: str, scale: tuple[int, int], pos: tuple[float, float]
    ) -> None:
        self.sprite = pygame.image.load(os.path.join("assets", sprite))
        self.scale = scale
        self.sprite = pygame.transform.scale(self.sprite, self.scale)
        self.pos = [pos[0], pos[1]]
        self.box = pygame.Rect(pos, self.scale)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.box.y = int(self.pos[1])
        self.box.x = int(self.pos[0])
        surface.blit(self.sprite, self.box)


class Projectile(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[float, float],
        speed: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.speed = speed
        self.alive = True

    def update(self, dt: float) -> None:
        if not self.alive:
            self.speed = 0
        self.pos[1] += self.speed * dt
        self.box.y = int(self.pos[1])

    def kill(self) -> None:
        self.alive = False


class Turret(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[int, int],
        velocity: float,
        fire_rate: float,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.velocity = velocity
        self.fire_rate = fire_rate
        self.speed = 0
        self.p_speed = -5 * self.velocity
        self.cd = 0
        self.hp = 3
        events_proxy.register(self, [EventID.BORDER_COLLISON, EventID.HIT])

    def update(self, dt: float) -> None:
        self.pos[0] += self.speed * dt
        self.cd -= dt
        self.box.x = int(self.pos[0])
        if self.hp == 0:
            events_proxy.emitte(Event(EventID.LOSE, []))

    def move(self, left: bool = False) -> None:
        self.speed = (-1 * self.velocity) if left else self.velocity

    def stop(self) -> None:
        self.speed = 0

    def notify(self, event: Event):
        if event.id == EventID.BORDER_COLLISON:
            self.pos[0] += event.data[0]
        if event.id == EventID.HIT:
            self.hp -= 1

    def shoot(self):
        if self.cd <= 0:
            self.cd = self.fire_rate
            return Projectile(
                "ammo.png",
                (20, 40),
                (self.pos[0] + self.scale[0] // 2 - 10, self.pos[1] - 40),
                self.p_speed,
            )


class SpaceShip(Entity):
    def __init__(
        self,
        sprite: str,
        scale: tuple[int, int],
        pos: tuple[float, float],
        speed: list[float],
        points: int,
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.speed = speed
        self.hp = 1
        self.change_course = False
        self.next_row = 0
        self.points = points
        self.boost = 0.5
        events_proxy.register(self, [EventID.SPEED_UP])

    def notify(self, event: Event) -> None:
        if event.id == EventID.SPEED_UP:
            x = abs(self.speed[0]) + event.data[0]
            if self.speed[0] < 0:
                x = -x
            self.speed[0] = x
            self.speed[1] += event.data[0]

    def change_direction(self, pos: float) -> None:
        self.next_row = 10
        self.change_course = not self.change_course
        self.speed[0] *= -1
        self.pos[0] = int(self.pos[0] + pos)

    def update(self, dt: float) -> None:
        if self.change_course:
            if self.next_row > 0:
                self.pos[1] += self.speed[1] * dt
                self.next_row -= self.speed[1] * dt
            else:
                self.change_course = False
        else:
            self.pos[0] += self.speed[0] * dt

    def hit(self) -> None:
        self.hp -= 1
        events_proxy.emitte(Event(EventID.SPEED_UP, [self.boost]))

    def kill(self):

        # add explosion on death
        pass

    def shoot(self):
        prj_speed = 70
        prj_size = (20, 40)
        return Projectile(
            "ammo.png",
            prj_size,
            (
                self.pos[0] + self.scale[0] // 2 - prj_size[0] // 2,
                self.pos[1] + prj_size[1],
            ),
            prj_speed,
        )


class Fleet:
    def __init__(
        self,
        fleet_size: tuple[int, int],
        top: int,
        rows: int,
        columns: int,
        speed: list[float],
        fire_chance: float,
    ) -> None:
        self.gap_x = 30
        self.gap_y = 30
        self.top = top
        self.fire_chance = fire_chance
        self.rows = rows
        self.columns = columns
        self.fleet_box = pygame.Rect(0, self.top, fleet_size[0], fleet_size[1])
        self.speed = speed
        self.fleet = []
        self.sprite_scale = (
            (self.fleet_box.width - 2 * self.gap_x - self.gap_x * self.columns)
            // self.columns,
            (self.fleet_box.height - 2 * self.gap_y) // self.rows,
        )
        self.create_fleet()
        events_proxy.register(self, [EventID.FLEET_COLLISION])

    def create_spaceship_line(self, y: int, sprite_name: str, points: int):
        x = self.gap_x
        line = []
        for _ in range(self.columns):
            line.append(
                SpaceShip(
                    sprite_name,
                    self.sprite_scale,
                    (x, y),
                    self.speed.copy(),
                    points,
                )
            )
            x += self.sprite_scale[0] + self.gap_x
        return line

    def create_fleet(self) -> None:
        y = self.gap_y + self.top
        self.fleet.append(self.create_spaceship_line(y, "top_ship.png", 30))
        y += self.sprite_scale[1] + 5
        self.fleet.append(self.create_spaceship_line(y, "mid_ship.png", 20))
        y += self.sprite_scale[1] + 5
        self.fleet.append(self.create_spaceship_line(y, "mid_ship.png", 20))
        y += self.sprite_scale[1] + 5
        self.fleet.append(self.create_spaceship_line(y, "bot_ship.png", 10))
        y += self.sprite_scale[1] + 5
        self.fleet.append(self.create_spaceship_line(y, "bot_ship.png", 10))

    def notify(self, event: Event) -> None:
        if event.id == EventID.FLEET_COLLISION:
            for line in self.fleet:
                for ship in line:
                    ship.change_direction(event.data[0])

    def update(self, dt: float) -> None:
        if len(self.fleet) == 0:
            events_proxy.emitte(Event(EventID.WIN, []))
        for line in self.fleet:
            for ship in line:
                ship.update(dt)
        num = random.random()
        if num <= self.fire_chance:
            selected = random.choice(self.fleet[-1])
            events_proxy.emitte(Event(EventID.SHOT_FIRED, [selected]))

    def clean(self) -> None:
        tmp_fleet = []
        for line in self.fleet:
            row = [ship for ship in line if ship.hp > 0]
            if row:
                tmp_fleet.append(row)
        self.fleet = tmp_fleet

    def draw(self, surface: pygame.Surface) -> None:
        for line in self.fleet:
            for ship in line:
                ship.draw(surface)


class Shield(Entity):
    def __init__(
        self, sprite: str, scale: tuple[int, int], pos: tuple[float, float]
    ) -> None:
        super().__init__(sprite, scale, pos)
        self.hp = 5

    def hit(self) -> None:
        self.hp -= 1

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
