import matrix
import math
from common import *
import render
from line import line
sin = lambda t: math.sin(t * math.pi / 180)
cos = lambda t: math.cos(t * math.pi / 180)
EDGE = 2
POLY = 3

class TransMatrix(object):
    def __init__(self, lst=-1, inv=-1):
        self.lst = matrix.id(4)
        self.inv = matrix.id(4)
        if lst != -1:
            self.lst = lst
        if inv != -1:
            self.inv = inv

    def __getitem__(self, i):
        return self.lst[i]

    def __setitem__(self, i, v):
        self.lst[i] = v

    def __str__(self):
        return matrix.toStr(self.lst)

    def __mul__(self, mat):
        if isinstance(mat, TransMatrix):
            return TransMatrix(matrix.multiply(self.lst, mat.lst), matrix.multiply(mat.inv, self.inv))
        elif isinstance(mat[0], tuple):  # point list (x,y,z)
            if isinstance(mat[0][0], Point):  # big p, in place
                for tri in mat:
                    for pt in tri:
                        x = self.lst[0][3] + pt.x*self.lst[0][0] + pt.y*self.lst[0][1] + pt.z*self.lst[0][2]
                        y = self.lst[1][3] + pt.x*self.lst[1][0] + pt.y*self.lst[1][1] + pt.z*self.lst[1][2]
                        z = self.lst[2][3] + pt.x*self.lst[2][0] + pt.y*self.lst[2][1] + pt.z*self.lst[2][2]
                        nx = self.inv[3][0] + pt.nx*self.inv[0][0] + pt.ny*self.inv[1][0] + pt.nz*self.inv[2][0]
                        ny = self.inv[3][1] + pt.nx*self.inv[0][1] + pt.ny*self.inv[1][1] + pt.nz*self.inv[2][1]
                        nz = self.inv[3][2] + pt.nx*self.inv[0][2] + pt.ny*self.inv[1][2] + pt.nz*self.inv[2][2]
                        pt.x, pt.y, pt.z = x, y, z
                        pt.nx, pt.ny, pt.nz = normalizedTuple((nx, ny, nz))
                return mat
            else:
                newls = []
                for pt in mat:
                    nx = self.lst[0][3]
                    ny = self.lst[1][3]
                    nz = self.lst[2][3]
                    for i in range(3):
                        nx += self.lst[0][i] * pt[i]
                        ny += self.lst[1][i] * pt[i]
                        nz += self.lst[2][i] * pt[i]
                    newls.append((nx,ny,nz))
                return newls
        else:  # matrix
            return matrix.multiply(self.lst, mat)

    def clone(self):
        newlst = [row[:] for row in self.lst]
        return TransMatrix(newlst)


def T(a, b, c):
    mat = TransMatrix()
    mat[0][3] = a
    mat[1][3] = b
    mat[2][3] = c
    mat.inv[0][3] = -a
    mat.inv[1][3] = -b
    mat.inv[2][3] = -c
    return mat

_inf = 1e33
def _rc(x):
    try:
        return 1./x
    except ZeroDivisionError:
        return _inf


def S(a, b, c):
    mat = TransMatrix()
    mat[0][0] = a
    mat[1][1] = b
    mat[2][2] = c
    mat.inv[0][0] = _rc(a)
    mat.inv[1][1] = _rc(b)
    mat.inv[2][2] = _rc(c)
    return mat


def R(axis, t, inv=True):
    mat = TransMatrix()
    c = cos(t)
    s = sin(t)
    if axis == 'z':
        mat[0][0] = c
        mat[0][1] = -s
        mat[1][0] = s
        mat[1][1] = c
    if axis == 'x':
        mat[1][1] = c
        mat[1][2] = -s
        mat[2][1] = s
        mat[2][2] = c
    if axis == 'y':
        mat[0][0] = c
        mat[0][2] = s
        mat[2][0] = -s
        mat[2][2] = c
    if inv:
        mat.inv = R(axis, -t, False).lst
    return mat


def C(cam):
    m = R('z', -cam.dz) * R('y', -cam.dy) * R('z', -cam.dz) * T(-cam.x, -cam.y, -cam.z)
    dt = TransMatrix()
    dt[3][3] = 0
    dt[3][2] = 1. / cam.vz
    dt[1][2] = -1.*cam.vy / cam.vz
    dt[0][2] = -1.*cam.vx / cam.vz
    return dt * m

def C2(cam, near, far):
    m = R('z', -cam.dz) * R('y', -cam.dy) * R('z', -cam.dz) * T(-cam.x, -cam.y, -cam.z)
    dt = TransMatrix()
    dt[0][0] = cam.vz
    dt[1][1] = cam.vz
    dt[3][2] = -1
    dt[3][3] = 0
    dt[2][2] = -1.*far / (far - near)
    dt[3][2] = -1.*far * near / (far - near)
    print dt * m
    return dt * m
def projected(m, cam):
    mp = C(cam) * m
    for i in xrange(len(mp[0])):
        for j in xrange(4):
            mp[j][i] /= mp[3][i]
    print mp
    return mp


def C3(r,t,n,f):
    mat = TransMatrix()
    mat[0][0] = 1.*n/r
    mat[1][1] = 1.*n/t
    mat[2][2] = -1.*(f+n)/(f-n)
    mat[2][3] = -2.*(f*n)/(f-n)
    mat[3][3] = 0
    mat[3][2] = -1
    return mat

def C3invT(r, t, n, f):
    mat = TransMatrix()
    mat[0][0] = 1.*r/n
    mat[1][1] = 1.*t/n
    mat[2][2] = 0
    mat[2][3] = 1.*(n-f)/(2*f*n)
    mat[3][2] = -1
    mat[3][3] = 1.*(f+n)/(2*f*n)
    return mat

'''
A =
n/r 0   0   0
0 n/t   0   0
0   0 -(f+n)/(f-n) -2fn/(f-n)
0   0  -1   0
A'A = I
A' =
r/n 0   ?
0 t/n   ?
0   0   ?
0   0   ?   ?
'''


def iparse(inp):
    return [float(i.strip()) for i in inp.split(' ')]



if __name__ == '__main__':  # parser
    from edgeMtx import edgemtx, addEdge, addTriangle, drawEdges, addBezier, addHermite, addCircle, drawTriangles
    from base import Image
    from render import drawObjectsNicely
    import render
    import shape
    cstack = [TransMatrix()]
    frc = 0
    cam = Camera(250, 250, 700, 90, 0, 0, -250, -250, 250)
    img = Image(500, 500)
    objects = []
    while(True):
        try:
            inp = raw_input('').strip()
        except EOFError:  # script file
            break
        if inp == 'line':
            inp = raw_input('')
            edges = edgemtx()
            addEdge(edges, *iparse(inp))
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'ident':
            cstack[-1] = TransMatrix()
        elif inp == 'scale':
            inp = raw_input('')
            cstack[-1] *= S(*iparse(inp))
        elif inp == 'move':
            inp = raw_input('')
            cstack[-1] *= T(*iparse(inp))
        elif inp == 'rotate':
            inp = raw_input('')
            axis, t = (i.strip() for i in inp.split(' '))
            cstack[-1] *= R(axis.lower(), float(t))
        elif inp == 'display':
            drawObjectsNicely(objects, img)
            img.flipUD().display()
        elif inp == 'save':
            drawObjectsNicely(objects, img)
            inp = raw_input('').strip()
            if inp[-4:] == '.ppm':
                img.flipUD().savePpm(inp)
            else:
                img.flipUD().saveAs(inp)
        elif inp == 'saveframe':
            drawObjectsNicely(objects, img)
            inp = raw_input('').strip()
            img.flipUD().savePpm('%s%d.ppm' % (inp, frc))
            frc += 1
        elif inp == 'circle':
            inp = raw_input('').strip()
            edges = edgemtx()
            addCircle(*[edges]+iparse(inp)+[.01])
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'bezier':
            inp = raw_input('').strip()
            edges = edgemtx()
            addBezier(*[edges]+iparse(inp)+[.01])
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'hermite':
            inp = raw_input('').strip()
            edges = edgemtx()
            addHermite(*[edges]+iparse(inp)+[.01])
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'clear':
            img = Image(500, 500)
        elif inp == 'clearstack':
            cstack = [TransMatrix()]
        elif inp == 'box':
            inp = raw_input('').strip()
            polys = edgemtx()
            coos = iparse(inp)
            shape.addBox(*[polys] + coos)
            polys = cstack[-1] * polys
            objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'sphere':
            inp = raw_input('').strip()
            polys = edgemtx()
            shape.addSphere(*[polys] + iparse(inp) + [.01])
            polys = cstack[-1] * polys
            objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'torus':
            inp = raw_input('').strip()
            polys = edgemtx()
            shape.addTorus(*[polys] + iparse(inp) + [.05, .05])
            polys = cstack[-1] * polys
            objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'push':
            cstack.append(cstack[-1].clone())
        elif inp == 'pop':
            cstack.pop()
        elif len(inp) < 1 or inp[0] != '#':
            print repr(inp), 'not valid'
