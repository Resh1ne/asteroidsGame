import pygame


class DestructionAnimation:
    def __init__(self, app, image, location):
        self.name = None
        self.app = app
        self.image = image
        self.location = location
        self.animation_duration = 500
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.animation_duration:
            self.app.main_group.remove(self)

    def draw(self, surface):
        surface.blit(self.image, self.location)
