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

        self.max_asteroids = 7
        self.asteroid_increase_interval = 10000
        self.last_asteroid_increase_time = pygame.time.get_ticks()

        self.game_over_font = pygame.font.SysFont("Arial", 64)
        self.is_game_over = False

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
            asteroid = self.create_asteroid_abroad(f"asteroid_{i}", 16, 32, WHITE)
            self.main_group.append(asteroid)

    def create_asteroid_abroad(self, name, min_radius, max_radius, color):
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        if direction[0] != 0:
            random_x = random.choice([-50, WIDTH + 50])
            random_y = random.randint(0, HEIGHT)
            direction = (1, 0) if random_x == -50 else (-1, 0)
        else:
            random_x = random.randint(0, WIDTH)
            random_y = random.choice([-50, HEIGHT + 50])
            direction = (0, 1) if random_y == -50 else (0, -1)
        radius = random.randint(min_radius, max_radius)
        asteroid = Asteroid(self, name, (random_x, random_y), radius, color)
        asteroid.velocity = Vector2D(direction[0] * random.randint(1, 3), direction[1] * random.randint(1, 3))
        return asteroid

    def increase_max_asteroids(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_asteroid_increase_time >= self.asteroid_increase_interval:
            self.max_asteroids += 1
            self.last_asteroid_increase_time = current_time

    def update(self):
        if not self.is_game_over:
            self.delta_time = self.clock.tick(FPS)
            self.increase_max_asteroids()
            for obj in self.main_group:
                obj.update(self.delta_time)
            if sum(isinstance(obj, Asteroid) for obj in self.main_group) < self.max_asteroids:
                asteroid = self.create_asteroid_abroad(f"asteroid_{len(self.main_group)}", 16, 32, WHITE)
                self.main_group.append(asteroid)
        self.check_game_over()

    def check_game_over(self):
        if self.player.health <= 0:
            self.is_game_over = True

    def draw_game_over_message(self):
        game_over_text = self.game_over_font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

    def restart_game(self):
        self.is_game_over = False
        self.__init__()

    def draw(self):
        self.screen.blit(self.srf_overlay, (0, 0))

        # draw the game object
        for obj in self.main_group:
            obj.draw(self.screen)

        pygame.display.flip()

        if self.is_game_over:
            self.draw_game_over_message()
            pygame.display.flip()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                if self.is_game_over:
                    self.restart_game()

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
