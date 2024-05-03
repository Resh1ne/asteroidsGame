import pygame

from bullet import Bullet
from settings import *
from subject import Subject


class Ship(Subject):
    def __init__(self, app, name, loc, radius, color):
        super(Ship, self).__init__(app, name, loc, radius, color)
        self.points_obj = OBJECT_POINTS['Player']['Ship-1']
        self.health = 10

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
                    if element.name != self.name and bullet.collision_check(element):
                        print("collision")
                        element.destroy()
                        bullets_to_remove.append(bullet)
                        break
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

    def shoot(self):
        bullet_direction = self.direction.normalize()  # Направление пули - направление корабля
        bullet_position = self.location + bullet_direction * self.radius  # Позиция пули - нос корабля
        # Создание экземпляра пули и добавление его в список пуль
        self.bullets.append(Bullet(self.app, bullet_position.xy, bullet_direction, self.bullet_speed))

    def collision(self):
        for element in self.app.main_group:
            if element.name != self.name:
                if self.collision_check(element):
                    if (pygame.time.get_ticks() - self.start_time) / 1000 > 1.5:
                        print("collision")
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
        pygame.draw.circle(surface, RED, self.location.xy, self.collision_dist, self.line_width)
        for bullet in self.bullets:
            bullet.draw(surface)
