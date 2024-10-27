from math import sqrt
from unittest import TestCase

from src.ex3.ex3 import computed_property


class TestComputedProperty(TestCase):
    def setUp(self) -> None:
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color

            @computed_property("x", "y", "z")
            def magnitude(self):
                return sqrt(self.x**2 + self.y**2 + self.z**2)

        self.vector_class = Vector

        return super().setUp()

    def test_computed_property_is_callable(self):
        x, y, z = 2, 2, 2
        vector = self.vector_class(x, y, z)
        self.assertTrue(True)

    def test_computed_property_applies_func(self):
        x, y, z = 2, 2, 2
        vector = self.vector_class(x, y, z)
        magnitude = vector.magnitude

        self.assertEqual(magnitude, sqrt(x**2 + y**2 + z**2))

    def test_compute_called_once_wo_params_change(self):
        x, y, z = 2, 2, 2
        vector = self.vector_class(x, y, z)
        magnitude1 = vector.magnitude
        magnitude2 = vector.magnitude

        self.assertEqual(magnitude1, magnitude2)

    def test_accepts_non_existing_params(self):
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color

            @computed_property("x", "y", "z", "non_existing")
            def magnitude(self):
                return sqrt(self.x**2 + self.y**2 + self.z**2)

        v = Vector(1, 1, 1)
        magnitude = v.magnitude

        self.assertTrue(True)

    def test_accepts_mote_than_one_computed_prop(self):
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color

            @computed_property("x", "y", "z", "non_existing")
            def magnitude(self):
                return sqrt(self.x**2 + self.y**2 + self.z**2)

            @computed_property("x", "y", "z")
            def soma(self):
                return self.x + self.y + self.z

        v = Vector(1, 1, 1)
        magnitude = v.magnitude
        soma = v.soma

        print(magnitude)
        print(soma)

        self.assertTrue(True)

    def test_computed_property_setter(self):
        class Circle:
            def __init__(self, radius=1):
                self.radius = radius

            @computed_property("radius", "area")
            def diameter(self):
                return self.radius * 2

            @diameter.setter
            def diameter(self, diameter):
                self.radius = diameter / 2

            @diameter.deleter
            def diameter(self):
                self.radius = 0

        first_rad = 1
        circle = Circle(first_rad)
        diameter = circle.diameter
        self.assertEqual(diameter, first_rad * 2)

        second_radius = 5
        circle.diameter = second_radius * 2

        self.assertEqual(circle.radius, second_radius)
        self.assertEqual(circle.diameter, second_radius * 2)

        del circle.diameter

        self.assertEqual(circle.radius, 0)
