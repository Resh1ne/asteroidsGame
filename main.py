import sys
import random
import pygame

from asteroid import Asteroid
from settings import *
from ship import Ship
from vector import Vector2D


class Game(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.srf_overlay = None
        self.main_group = None
        self.asteroids = None
        self.player = None
        self.asteroid = None
        self.max_asteroids = 10

        self.is_running = True
        self.delta_time = 0.01
        self.time = 0

        self.on_init()

    def on_init(self):
        self.main_group = list()
        self.srf_overlay = pygame.Surface((WIDTH, HEIGHT))
        self.srf_overlay.set_alpha(ALPHA)

        self.player = Ship(self, "player", (WIDTH // 2, HEIGHT // 2), 16, WHITE)
        self.main_group.append(self.player)
        for i in range(self.max_asteroids):
            random_x = random.randint(0, WIDTH)
            random_y = random.randint(0, HEIGHT)
            self.main_group.append(
                Asteroid(self, f"asteroid_{i}", (random_x, random_y), 32, WHITE)
            )
        # for i in range(10):
        #     # Создание астероида за пределами экрана с рандомной координатой X
        #     random_x = random.randint(0, WIDTH)
        #     asteroid = Asteroid(self, f"asteroid_{i}", (random_x, -50), 32, WHITE)
        #     # Задаем начальную скорость и направление движения астероида
        #     asteroid.velocity = Vector2D(0, 3)  # Скорость 3 пикселя вниз
        #     asteroid.direction = Vector2D(0, 1)  # Направление движения вниз
        #     self.main_group.append(asteroid)

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        for obj in self.main_group:
            obj.update(self.delta_time)
            # Если астероидов не максимально количество, то добавляем до максимального
        if sum(isinstance(obj, Asteroid) for obj in self.main_group) < self.max_asteroids:
            random_x = random.randint(0, WIDTH)
            random_y = random.randint(0, HEIGHT)
            self.main_group.append(
                Asteroid(self, f"asteroid_{len(self.main_group)}", (random_x, random_y), 32, WHITE)
            )
        # if sum(isinstance(obj, Asteroid) for obj in self.main_group) < self.max_asteroids:
        #     random_x = random.randint(0, WIDTH)
        #     asteroid = Asteroid(self, f"asteroid_{len(self.main_group)}", (random_x, -50), 32, WHITE)
        #     asteroid.velocity = Vector2D(0, 3)
        #     asteroid.direction = Vector2D(0, 1)
        #     self.main_group.append(asteroid)

    def draw(self):
        self.screen.blit(self.srf_overlay, (0, 0))

        # draw the game object
        for obj in self.main_group:
            obj.draw(self.screen)

        pygame.display.flip()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

    def run(self):
        while self.is_running:
            self.event_handler()
            self.update()
            self.draw()
        else:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
