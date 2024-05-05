import pygame

from settings import *
from vector import Vector2D


class Bullet(object):
    def __init__(self, app, loc, direction, speed):
        self.app = app
        self.location = Vector2D(loc[0], loc[1])
        self.direction = direction
        self.speed = speed
        self.color = WHITE
        self.radius = 2
        self.collision_dist = self.radius / 1.2

    def collision_check(self, other):
        dist_vec = self.location.distance(other.location)
        dist_rad = self.collision_dist + other.collision_dist
        if dist_vec <= dist_rad:
            return True

    def update(self, dt):
        self.location += self.direction * self.speed * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.location.x), int(self.location.y)), self.radius)
