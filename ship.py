import pygame

from animation import DestructionAnimation
from bullet import Bullet
from settings import *
from subject import Subject


class Ship(Subject):
    def __init__(self, app, name, loc, radius, color):
        super(Ship, self).__init__(app, name, loc, radius, color)
        self.points_obj = OBJECT_POINTS['Player']['Ship-1']
        self.health = 3

        self.bullets = []
        self.bullet_speed = 0.5

        self.start_time = pygame.time.get_ticks()

    def destroy_bullet(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            if bullet.location.x < 0 or bullet.location.x > WIDTH or \
                    bullet.location.y < 0 or bullet.location.y > HEIGHT:
                bullets_to_remove.append(bullet)
            else:
                for element in self.app.main_group:
                    if element.name != self.name and not isinstance(element,
                                                                    DestructionAnimation) and bullet.collision_check(
                            element):
                        self.app.hit.play()
                        element.destroy()
                        self.app.increase_score(100)
                        bullets_to_remove.append(bullet)
                        break
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

    def shoot(self):
        self.app.shoot.play()
        bullet_direction = self.direction.normalize()
        bullet_position = self.location + bullet_direction * self.radius
        self.bullets.append(Bullet(self.app, bullet_position.xy, bullet_direction, self.bullet_speed))

    def collision(self):
        for element in self.app.main_group:
            if element.name != self.name and not isinstance(element, DestructionAnimation):
                if self.collision_check(element):
                    if (pygame.time.get_ticks() - self.start_time) / 1000 > 1.0:
                        self.app.fail.play()
                        self.start_time = pygame.time.get_ticks()
                        self.health -= 1
                        element.destroy()

    def management(self, dt):
        self.direction.x, self.direction.y = self.get_angle(self.rotation_angle, 90)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotation_angle += self.rotation_speed * dt
        if keys[pygame.K_d]:
            self.rotation_angle -= self.rotation_speed * dt
        if keys[pygame.K_w]:
            self.direction.normalize()
            self.velocity.x += (self.direction.x / 2) * (self.get_speed(dt) / 2)
            self.velocity.y += (self.direction.y / 2) * (self.get_speed(dt) / 2)

    def update(self, dt):
        self.collision()
        self.reset_angle()
        self.management(dt)
        self.movement()
        for bullet in self.bullets:
            bullet.update(dt)
        self.destroy_bullet()
        self.keep_within_screen_bounds()

    def keep_within_screen_bounds(self):
        if self.location.x < 0:
            self.location.x = 0
        elif self.location.x > WIDTH:
            self.location.x = WIDTH

        if self.location.y < 0:
            self.location.y = 0
        elif self.location.y > HEIGHT:
            self.location.y = HEIGHT

    def render_health(self, surface):
        for i in range(1, self.health + 1):
            pygame.draw.lines(surface, self.color, True,
                              self.points(self.radius / 2, self.points_obj, 0,
                                          ((self.radius * 1.2) * i, (self.radius * 1.2))),
                              self.line_width)

    def draw(self, surface):
        self.render_health(surface)
        pygame.draw.lines(surface, self.color, True,
                          self.points(self.radius, self.points_obj, self.rotation_angle, self.location.xy),
                          self.line_width)
        for bullet in self.bullets:
            bullet.draw(surface)
