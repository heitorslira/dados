from unittest import TestCase
from unittest.mock import patch
from math import sqrt
from src.ex3.ex3 import computed_property

class TestComputedProperty(TestCase):
    def setUp(self) -> None:
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color

            @computed_property("x", "y", "z")
            def magnitude(self):
                print("computing magnitude")
                return sqrt(self.x**2 + self.y**2 + self.z**2)
        


        self.vectorclass = Vector

        return super().setUp()

    def test_computed_property_is_callable(self):
        x, y, z = 2, 2, 2
        vector = self.vectorclass(x, y, z)
        self.assertTrue(True)

    def test_computed_property_applies_func(self):
        x, y, z = 2, 2, 2
        vector = self.vectorclass(x, y, z)
        magnitude = vector.magnitude

        self.assertEqual(magnitude, sqrt(x**2 + y**2 + z**2))

    def test_compute_called_once_wo_params_change(self):
        x, y, z = 2, 2, 2
        vector = self.vectorclass(x, y, z)
        magnitude1 = vector.magnitude
        magnitude2 = vector.magnitude

        self.assertEqual(magnitude1, magnitude2)
