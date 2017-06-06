class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, o):
        self.x+=o.x
        self.y+=o.y
        return self

    def __add__(self, o):
        return Vec2(self.x+o.x,self.y+o.y)

    def __isub__(self, o):
        self.x-=o.x
        self.y-=o.y
        return self

    def __sub__(self, o):
        return Vec2(self.x-o.x,self.y-o.y)

    def __imul__(self, o):
        self.x*=o
        self.y*=o
        return self
    
    def __mul__(self, o):
        return Vec2(self.x*o,self.y*o)

    def __idiv__(self, o):
        self.x/=o
        self.y/=o
        return self
    
    def __div__(self, o):
        return Vec2(self.x/o,self.y/o)

    def cross(self, o):
        return self.x*o.y - self.y*o.x

class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iadd__(self, o):
        self.x+=o.x
        self.y+=o.y
        self.z+=o.z
        return self
    
    def __add__(self, o):
        return Vec3(self.x+o.x,self.y+o.y,self.z+o.z)

    def __isub__(self, o):
        self.x-=o.x
        self.y-=o.y
        self.z-=o.z
        return self
    
    def __sub__(self, o):
        return Vec3(self.x-o.x,self.y-o.y,self.z-o.z)

    def __imul__(self, o):
        self.x*=o
        self.y*=o
        self.z*=o
        return self
    
    def __mul__(self, o):
        return Vec3(self.x*o,self.y*o,self.z*o)

    def __idiv__(self, o):
        self.x/=o
        self.y/=o
        self.z/=o
        return self
    
    def __div__(self, o):
        return Vec3(self.x/o,self.y/o,self.z/o)

    def cons(o1, o2):
        if isinstance(o1, Vec2):
            return Vec3(o1.x, o1.y, o2)
        return Vec3(o1, o2.x, o2.y)

    def cross(self, o):
        return Vector(self.y*o.z-self.z*o.y, self.z*o.x-self.x*o.z, self.x*o.y-self.y*o.x)

    def lvec(self):
        return Vec2(self.x, self.y)

    def rvec(self):
        return Vec2(self.y, self.z)


class Vec4(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __iadd__(self, o):
        self.x+=o.x
        self.y+=o.y
        self.z+=o.z
        self.w+=o.w
        return self
    
    def __add__(self, o):
        return Vec4(self.x+o.x,self.y+o.y,self.z+o.z,self.w+o.w)

    def __isub__(self, o):
        self.x-=o.x
        self.y-=o.y
        self.z-=o.z
        self.w-=o.w
        return self
    
    def __sub__(self, o):
        return Vec4(self.x-o.x,self.y-o.y,self.z-o.z,self.w-o.w)

    def __imul__(self, o):
        self.x*=o
        self.y*=o
        self.z*=o
        self.w*=o
        return self
    
    def __mul__(self, o):
        return Vec4(self.x*o,self.y*o,self.z*o,self.w*o)

    def __idiv__(self, o):
        self.x/=o
        self.y/=o
        self.z/=o
        self.w/=o
        return self
    
    def __div__(self, o):
        return Vec4(self.x/o,self.y/o,self.z/o,self.w/o)

    def cons(o1, o2):
        if isinstance(o1, Vec3):
            return Vec4(o1.x, o1.y, o1.z, o2)
        return Vec4(o1, o2.x, o2.y, o2.z)

    def lvec(self):
        return Vec3(self.x, self.y, self.z)

    def rvec(self):
        return Vec3(self.y, self.z, self.w)
