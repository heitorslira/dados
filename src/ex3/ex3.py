class computed_property:
    def __init__(self, *args):
        self.args = args
        self.computed_once = False
        self.cached_value = None

    def __call__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.params = {arg: None for arg in self.args}
        return self

    def __get__(self, instance, owner):
        if not self.computed_once:
            self.computed_once = True
            self.params = {arg: None for arg in self.args}
            computed_value = self._compute(instance)
            return computed_value
        if self._check_params_changed(instance):
            computed_value = self._compute(instance)
            return computed_value
        else:
            return self.cached_value

    def setter(self, func):
        self.setter_func = func

        return self

    def __set__(self, instance, value):
        self.setter_func(instance, value)
        self.computed_once = False

    def deleter(self, func):
        self.deleter_func = func

        return self

    def __delete__(self, instance):
        self.deleter_func(instance)

    def _compute(self, instance):
        print(f"computing {self.func.__name__}")
        calculated_attrib = self.func(instance)
        self.cached_value = calculated_attrib
        self._set_cahced_attribs(instance)

        return self.cached_value

    def _check_params_changed(self, instance):
        for param, value in self.params.items():
            try:
                attrib = getattr(instance, param)
            except AttributeError:
                continue
            if value != attrib:
                return True
        return False

    def _set_cahced_attribs(self, instance):
        for param in self.params:
            try:
                self.params[param] = getattr(instance, param)
            except AttributeError:
                continue


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property("radius", "area")
    def diameter(self):
        """Circle diameter from radius"""
        return self.radius * 2


from math import sqrt


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property("x", "y", "z")
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)


def vector():
    v = Vector(9, 2, 6)
    print(v.magnitude)

    v.color = "red"
    print(v.magnitude)

    v.y = 18
    print(v.magnitude)


def circle():
    circle = Circle()
    print(circle.diameter)
    print(circle.diameter)
    print(circle.diameter)

    circle.radius = 10
    print(circle.diameter)


if __name__ == "__main__":
    vector()
    circle()
