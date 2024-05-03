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
        self.direction.normalize()

        self.movement()
        self.check_collision_with_asteroids()

    def check_collision_with_asteroids(self):
        if self.location.x > WIDTH or self.location.y > HEIGHT:
            self.destroy()
        for element in self.app.main_group:
            if isinstance(element, Asteroid) and element != self:
                if self.collision_check(element):
                    self.destroy()
                    element.destroy()
                    break

    def destroy(self):
        if self in self.app.main_group:
            self.app.main_group.remove(self)

    def draw(self, surface):
        pygame.draw.lines(surface, self.color, True,
                          self.points(self.radius, self.points_obj, self.rotation_angle, self.location.xy),
                          self.line_width)
