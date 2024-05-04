import random
import sys

import pygame

from settings import *


class Menu:
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.font = pygame.font.SysFont("Arial", 36)
        self.menu_items = ["Start Game", "Table of Records", "Help", "Quit"]
        self.selected_item = 0
        self.is_visible = True

        # self.records = [
        #     ("Player 1", 500),
        #     ("Player 2", 300),
        #     ("Player 3", 700),
        #     ("Player 4", 400),
        #     ("Player 5", 900)
        # ]

    def draw(self):
        if self.is_visible:
            self.screen.fill((0, 0, 0))
            for index, item in enumerate(self.menu_items):
                color = (255, 255, 255) if index == self.selected_item else (128, 128, 128)
                text = self.font.render(item, True, color)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 50))
                self.screen.blit(text, text_rect)

    def draw_records(self):
        records_shown = True
        while records_shown:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    records_shown = False
            self.app.records.sort(key=lambda x: x[1], reverse=True)
            for i, (name, score) in enumerate(self.app.records, start=1):
                text = self.font.render(f"{name}: {score}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                self.screen.blit(text, text_rect)
            pygame.display.flip()

    def draw_help(self):
        help_shown = True
        while help_shown:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    help_shown = False
            help_text = [
                "Controls:",
                "Use arrow keys to move the ship.",
                "Press SPACE to shoot.",
                "Avoid asteroids and survive!",
                "Press ESCAPE to return to the menu."
            ]
            for i, line in enumerate(help_text):
                text = self.font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                self.screen.blit(text, text_rect)
            pygame.display.flip()

    def handle_events(self, event):
        if self.is_visible:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.selected_item == 0:  # Start Game
                        self.is_visible = False
                    elif self.selected_item == 1:  # Table
                        self.draw_records()
                    elif self.selected_item == 2:  # Helper
                        self.draw_help()
                    elif self.selected_item == 3:  # Quit
                        pygame.quit()
                        sys.exit()
