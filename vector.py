import math


class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y

    def __add__(self, other):
        """Сложение двух векторов"""
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type")

    def __sub__(self, other):
        """Вычитание одного вектора из другого"""
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type")

    def __mul__(self, other):
        """Поэлементное умножение двух векторов"""
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type")

    def __truediv__(self, scalar):
        """Деление вектора на скаляр числа"""
        if scalar != 0:
            return Vector2D(self.x / scalar, self.y / scalar)
        else:
            raise TypeError("Division by zero is not allowed")

    def magnitude(self):
        """Вычисление длины (модуля) вектора"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def normalize(self):
        """Нормализация вектора (приведение к единичной длине)"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(round(self.x / mag, 2), round(self.y / mag, 2))

    def dot_product(self, other):
        """Скалярное произведение векторов"""
        return (self.x * other.x) + (self.y * other.y)

    def angle_with(self, other):
        """Угол между двумя векторами в радианах"""
        mag_self = self.magnitude()
        mag_other = other.magnitude()

        if mag_self == 0 or mag_other == 0:
            raise ValueError("Cannot compute angle with zero-length vector")

        dot = self.dot_product(other)
        cos_theta = dot / (mag_self * mag_other)
        return math.acos(cos_theta)

    def limit(self, max_value):
        mag = self.magnitude()
        if mag > max_value:
            ratio = max_value / mag
            self.x *= ratio
            self.y *= ratio
