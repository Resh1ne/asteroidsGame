import random

import pygame

from settings import *
from subject import Subject


class Asteroid(Subject):
    def __init__(self, app, name, loc, radius, color):
        super(Asteroid, self).__init__(app, name, loc, radius, color)
        self.points_obj = OBJECT_POINTS['Enemy']['Asteroid-1']

    def update(self, dt):
        self.reset_angle()

        self.rotation_angle += self.rotation_speed * dt
        # self.direction.x, self.direction.y = self.get_angle(self.rotation_angle, 90)
        self.direction.normalize()
        # self.velocity.x += (self.direction.x / 2) * (self.get_speed(dt) / 2)
        # self.velocity.y += (self.direction.y / 2) * (self.get_speed(dt) / 2)

        self.movement()
        if self.location.y > HEIGHT or self.location.x > WIDTH:
            self.app.main_group.remove(self)

    def destroy(self):
        if self in self.app.main_group:
            self.app.main_group.remove(self)

    def draw(self, surface):
        pygame.draw.lines(surface, self.color, True,
                          self.points(self.radius, self.points_obj, self.rotation_angle, self.location.xy),
                          self.line_width)
        if self.collision_check(self.app.player):
            pygame.draw.circle(surface, BLUE, self.location.xy, self.collision_dist, self.line_width)
        else:
            pygame.draw.circle(surface, RED, self.location.xy, self.collision_dist, self.line_width)
