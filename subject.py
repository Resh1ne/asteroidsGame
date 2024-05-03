import math

from vector import Vector2D


class Subject(object):
    def __init__(self, app, name, loc, radius, color):
        self.app = app
        self.radius = radius
        self.color = color
        self.name = name

        self.health = 0

        self.location = Vector2D(loc[0], loc[1])
        self.velocity = Vector2D(0, 0)
        self.direction = Vector2D(0, 0)

        self.line_width = 1
        self.zeroing_out = 90

        self.collision_dist = self.radius/1.2

        self.max_speed = 3.5
        self.movement_speed = 0.05
        self.rotation_speed = 0.18
        self.rotation_angle = 0.0

        self.points_obj = None

    def get_speed(self, dt):
        return self.movement_speed * dt

    def reset_angle(self):
        self.rotation_angle = 0 if self.rotation_angle > 360 else self.rotation_angle

    def get_angle(self, angle, add_angle) -> tuple:
        return (
            math.sin(math.radians(angle + add_angle + self.zeroing_out)),
            math.cos(math.radians(angle + add_angle + self.zeroing_out))
        )

    def get_point_position(self, distance, angle, add_angle, loc) -> tuple:
        angle_sin, angle_cos = self.get_angle(angle, add_angle)
        return (
            distance * angle_sin + loc[0],
            distance * angle_cos + loc[1],
        )

    def points(self, radius, obj, rotate_angle, loc) -> list:
        return [
            self.get_point_position(radius / obj['radius'][index], rotate_angle, angle, loc)
            for index, angle in enumerate(obj['angles'])
        ]

    def movement(self):
        self.velocity.limit(self.max_speed)
        self.location += self.velocity

    def collision_check(self, other):
        dist_vec = self.location.distance(other.location)
        dist_rad = self.collision_dist + other.collision_dist
        if dist_vec <= dist_rad:
            return True

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
