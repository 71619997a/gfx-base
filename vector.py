class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Vec2(self.x+o.x, self.y+o.y)

    def __mul__(self, o):
        return self.x*o.x + self.y*o.y

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y

    def cross(self, o):
        return self.x*o.y - self.y*o.x
        
class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def from(o1, o2):
        if isinstance(o1, Vec2):
            return Vec3(o1.x, o1.y, o2)
        return Vec3(o1, o2.x, o2.y)
        
    def __add__(self, o):
        return Vector(self.x+o.x, self.y+o.y, self.z+o.z)

    def __mul__(self, o):
        return self.x*o.x + self.y*o.y + self.z*o.z
    
    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        self.z += o.z

    def cross(self, o):
        return Vector(self.y*o.z-self.z*o.y, self.z*o.x-self.x*o.z, self.x*o.y-self.y*o.x)

class Vec4(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, o):
        return Vector(self.x+o.x, self.y+o.y, self.z+o.z, self.w+o.w)

    def __mul__(self, o):
        return self.x*o.x + self.y*o.y + self.z*o.z + self.w*o.w

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        self.z += o.z
        self.w += o.w

