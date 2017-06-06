import math

class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return 2
        
    def __neg__(self):
        return Vec2(-self.x, -self.y)

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

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError('Attempted to get index %s of a Vec2.' % (str(i)))

    def __setitem__(self, i, v):
        if i == 0:
            self.x = v
        elif i == 1:
            self.y = v
        else:
            raise IndexError('Attempted to get index %s of a Vec2.' % (str(i)))

    def __repr__(self):
        return 'Vec2(%s, %s)' % (str(self.x), str(self.y))

    def __str__(self):
        return repr(self)
        
    def __hash__(self):
        return hash((self.x, self.y))

    def post(self, i):
        return Vec3(self.x, self.y, i)

    def pre(self, i):
        return Vec3(i, self.x, self.y)
        
    def cross(self, o):
        return self.x*o.y - self.y*o.x

    def dot(self, o):
        return self.x*o.x + self.y*o.y

    def same(self, x, y):
        return self.x == x and self.y == y

    def clone(self):
        return Vec2(self.x, self.y)

    def norm(self):
        return math.sqrt(self.dot(self))
    
    def normalize(self):
        self /= self.norm()

    def normalized(self):
        return self / self.norm()

    def set(self, x, y):
        self.x = x
        self.y = y

class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __len__(self):
        return 3
        
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
        
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

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError('Attempted to get index %s of a Vec3.' % (str(i)))

    def __setitem__(self, i, v):
        if i == 0:
            self.x = v
        elif i == 1:
            self.y = v
        elif i == 2:
            self.z = v
        else:
            raise IndexError('Attempted to get index %s of a Vec3.' % (str(i)))

    def __repr__(self):
        return 'Vec3(%s, %s, %s)' % (str(self.x), str(self.y), str(self.z))

    def __str__(self):
        return repr(self)
        
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def post(self, i):
        return Vec4(self.x, self.y, self.z, i)

    def pre(self, i):
        return Vec4(i, self.x, self.y, self.z)
    
    def cross(self, o):
        return Vec3(self.y*o.z-self.z*o.y, self.z*o.x-self.x*o.z, self.x*o.y-self.y*o.x)

    def lvec(self):
        return Vec2(self.x, self.y)

    def rvec(self):
        return Vec2(self.y, self.z)

    def dot(self, o):
        return self.x*o.x + self.y*o.y + self.z*o.z

    def same(self, x, y, z):
        return self.x == x and self.y == y and self.z == z

    def clone(self):
        return Vec3(self.x, self.y, self.z)

    def norm(self):
        return math.sqrt(self.dot(self))
    
    def normalize(self):
        self /= self.norm()

    def normalized(self):
        print self, self.norm()
        return self / self.norm()

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Vec4(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __len__(self):
        return 4

    def __neg__(self):
        return Vec4(-self.x, -self.y, -self.z, -self.w)
        
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

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        elif i == 3:
            return self.w
        else:
            raise IndexError('Attempted to get index %s of a Vec4.' % (str(i)))

    def __setitem__(self, i, v):
        if i == 0:
            self.x = v
        elif i == 1:
            self.y = v
        elif i == 2:
            self.z = v
        elif i == 3:
            self.w = v
        else:
            raise IndexError('Attempted to get index %s of a Vec4.' % (str(i)))

    def __repr__(self):
        return 'Vec4(%s, %s, %s, %s)' % (str(self.x), str(self.y), str(self.z), str(self.w))

    def __str__(self):
        return repr(self)
        
    def __hash__(self):
        return hash((self.x, self.y, self.z, self.w))

    def lvec(self):
        return Vec3(self.x, self.y, self.z)

    def rvec(self):
        return Vec3(self.y, self.z, self.w)

    def dot(self, o):
        return self.x*o.x + self.y*o.y + self.z*o.z + self.w*o.w

    def same(self, x, y, z, w):
        return self.x == x and self.y == y and self.z == z and self.w == w

    def clone(self):
        return Vec4(self.x, self.y, self.z, self.w)

    def norm(self):
        return math.sqrt(self.dot(self))
    
    def normalize(self):
        self /= self.norm()

    def normalized(self):
        return self / self.norm()

    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
