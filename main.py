import random
import sys

import pygame

from asteroid import Asteroid
from menu import Menu
from settings import *
from ship import Ship
from vector import Vector2D


class Game(object):
    records = [
        ("Player 1", 500),
        ("Player 2", 300),
        ("Player 3", 700),
        ("Player 4", 400),
        ("Player 5", 900)
    ]

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

        self.score = 0

        self.max_asteroids = 7
        self.asteroid_increase_interval = 10000
        self.last_asteroid_increase_time = pygame.time.get_ticks()

        self.game_over_font = pygame.font.SysFont("Arial", 64)
        self.game_over_drawn = False
        self.is_game_over = False

        self.is_running = True
        self.delta_time = 0.01
        self.time = 0

        self.menu = Menu(self.screen, self)
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
        game_over_text = self.game_over_font.render("Game Over", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()

    def increase_score(self, points):
        self.score += points

    def draw_score(self):
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        text_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        self.screen.blit(score_text, text_rect)

    def restart_game(self):
        self.is_game_over = False
        self.__init__()

    def draw(self):
        # self.screen.blit(self.srf_overlay, (0, 0))
        self.screen.fill((0, 0, 0))

        # draw the game object
        for obj in self.main_group:
            obj.draw(self.screen)
        self.draw_score()
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
            if self.menu.is_visible:
                self.menu.draw()
                pygame.display.flip()
                self.menu.handle_events(pygame.event.poll())
            else:
                self.event_handler()
                self.update()
                self.draw()

                if self.is_game_over:
                    if self.check_high_score():
                        self.show_high_score_dialog()
                        self.restart_game()
        else:
            pygame.quit()
            sys.exit()

    def check_high_score(self):
        for record in Game.records:
            if self.score >= record[1]:
                return True
        return False

    def save_high_score(self, name):
        # Проходим по каждой записи в таблице рекордов
        for i, record in enumerate(Game.records):
            # Если текущий результат больше или равен результату в текущей записи
            if self.score >= record[1]:
                # Вставляем новую запись перед текущей записью
                Game.records.insert(i, (name, self.score))
                # Удаляем последнюю запись, если таблица переполнена
                if len(Game.records) > 5:
                    Game.records.pop()
                return
        # # Если текущий результат не превышает ни одного рекорда, добавляем его в конец таблицы
        # self.menu.records.append((name, self.score))

    def show_high_score_dialog(self):
        # Показать диалоговое окно с поздравлением
        # self.menu.is_visible = True
        # self.menu.selected_item = 1  # Выбрать "Table of Records"
        # self.menu.draw()
        # pygame.display.flip()
        name = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return
                    else:
                        name += event.unicode
            self.screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 36)
            text = font.render(f"Congratulations! You've got a high score of {self.score}!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)
            text = font.render("Enter your name:", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(text, text_rect)
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
        self.save_high_score(name)


if __name__ == "__main__":
    game = Game()
    game.run()
