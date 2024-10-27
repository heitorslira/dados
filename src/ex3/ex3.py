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

    def _compute(self, instance):
        print(f"computing {self.func.__name__}")
        calculated_attrib = self.func(instance)
        self.cached_value = calculated_attrib
        self._set_cahced_attribs(instance)

        return self.cached_value

    def _check_params_changed(self, instance):
        for param, value in self.params.items():
            if value != getattr(instance, param):
                return True
        return False

    def _set_cahced_attribs(self, instance):
        for param in self.params:
            self.params[param] = getattr(instance, param)


def vector():
    from math import sqrt
    class Vector:
        def __init__(self, x, y, z, color=None):
            self.x, self.y, self.z = x, y, z
            self.color = color 
        @computed_property('x', 'y', 'z')
        def magnitude(self):
            return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    v = Vector(9, 2, 6)
    print(v.magnitude)
    
    v.color = 'red'
    print(v.magnitude)
    
    v.y = 18
    print(v.magnitude)
    
    
def circle():
    class Circle:
        def __init__(self, radius=1):
            self.radius = radius
        
        
        @computed_property('radius', 'area')
        def diameter(self):
            return self.radius * 2
    
    circle = Circle()
    circle.diameter

if __name__ == '__main__':
    # vector()
    circle()