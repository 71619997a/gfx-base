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
    def __init__(self, lst=-1, invt=-1):
        self.lst = matrix.id(4)
        for i in xrange(4):
            self.lst[i] = Vec4(*self.lst[i])
        self.invT = matrix.id(4)
        for i in xrange(4):
            self.invT[i] = Vec4(*self.invT[i])
        if lst != -1:
            self.lst = lst
        if invt != -1:
            self.invT = invt

    def __getitem__(self, i):
        return self.lst[i]

    def __setitem__(self, i, v):
        self.lst[i] = v

    def __str__(self):
        return matrix.toStr(self.lst)

    def __mul__(self, mat):
        if isinstance(mat, TransMatrix):
            return TransMatrix(matrix.multiply(self.lst, mat.lst), matrix.multiply(mat.invT, self.invT))
        elif isinstance(mat[0], tuple):  # point list (x,y,z
            checkP = not self.lst[3].same(0, 0, 0, 1)
            if isinstance(mat[0][0], Point):  # big p, in place
                for tri in mat:
                    for pt in tri:
                        pt.P = pt.P.post(1.)
                        pt.N = pt.N.post(1.)
                        x = self.lst[0].dot(pt.P)
                        y = self.lst[1].dot(pt.P)
                        z = self.lst[2].dot(pt.P)
                        if checkP:
                            w = self.lst[3].dot(pt.P)
                            if w != 1:
                                rw = 1./w
                                x *= rw
                                y *= rw
                                z *= rw
                        nx = self.invT[0].dot(pt.N)
                        ny = self.invT[1].dot(pt.N)
                        nz = self.invT[2].dot(pt.N)
                        pt.P = Vec3(x, y, z)
                        pt.N = Vec3(nx, ny, nz)
                        pt.N.normalize()
                return mat
            else:
                return []
        elif isinstance(mat[0], Vec3):
            newls = []
            for pt in mat:
                pt = pt.post(1.)
                nx = pt.dot(self.lst[0])
                ny = pt.dot(self.lst[1])
                nz = pt.dot(self.lst[2])
                newls.append(Vec3(nx, ny, nz))
            return newls
        else:  # matrix
            return matrix.multiply(self.lst, mat)

    def clone(self):
        newlst = [i.clone() for i in self.lst]
        newit  = [i.clone() for i in self.invT]
        return TransMatrix(newlst, newit)

    def transpose(self):
        newme = TransMatrix()
        for i in xrange(4):
            newme.lst[i] = Vec4(*[vec[i] for vec in self.lst])
            newme.invT[i] = Vec4(*[vec[i] for vec in self.invT])
        return newme


def T(a, b, c):
    mat = TransMatrix()
    mat[0][3] = a
    mat[1][3] = b
    mat[2][3] = c
    mat.invT[3][0] = -a
    mat.invT[3][1] = -b
    mat.invT[3][2] = -c
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
    mat.invT[0][0] = _rc(a)
    mat.invT[1][1] = _rc(b)
    mat.invT[2][2] = _rc(c)
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
        mat.invT = R(axis, -t, False).lst.transpose()
    return mat

def V(cam):
    return R('x', -cam.dx) * R('y', -cam.dy) * R('z', -cam.dz) * T(-cam.x, -cam.y, -cam.z)

def perspective(fovx, fovy, n, f=None):
    mat = TransMatrix()
    invT = mat.invT
    wx = 1 / math.tan(fovx*math.pi/360.)
    wy = 1 / math.tan(fovy*math.pi/360.)
    mat[0][0] = wx
    mat[1][1] = wy
    mat[3][3] = 0
    mat[3][2] = -1
    invT[0][0] = 1./wx
    invT[1][1] = 1./wy
    invT[2][2] = 0
    invT[3][2] = -1
    if f is not None:
        mat[2][2] = (f+n+0.)/(n-f)
        tnf = 2.*n*f
        mat[2][3] = tnf/(n-f)
        invT[2][3] = (n-f)/tnf
        invT[3][3] = (f+n)/tnf
    else:
        mat[2][2] = -1
        tn = 2.*n
        mat[2][3] = -tn
        invT[2][3] = -1/tn
        invT[3][3] = 1/tn
    return mat

def lookat(cam, objP):
    objP = cam.P - objP
    V = objP.normalized()
    W = V.cross(cam.U).normalized()
    U = W.cross(V)
    mat = TransMatrix()
    mat[0] = W.post(0.)
    mat[1] = U.post(0.)
    mat[2] = -V.post(0.)
    mat.invT = mat.clone().lst
    mat[0][3] = W.dot(cam.P)
    mat[1][3] = -U.dot(cam.P)
    mat[2][3] = V.dot(cam.P)
    mat.invT[3][0] = -dot(mat[0][3], mat[1][3], mat[2][3],mat[0][0], mat[1][0], mat[2][0])
    mat.invT[3][1] = -dot(mat[0][3], mat[1][3], mat[2][3],mat[0][1], mat[1][1], mat[2][1])
    mat.invT[3][2] = -dot(mat[0][3], mat[1][3], mat[2][3],mat[0][2], mat[1][2], mat[2][2])
    #print mat
    #print TransMatrix(mat.inv)
    #print TransMatrix(matrix.multiply(mat.lst, mat.inv))
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
    cam = Camera(Vec3(100,20,30),Vec3(1,0,0))
    t = lookat(cam, Vec3(50, 50, 50))
    # t = V(cam)
    l = [-50,50]
    for i in l:
        for j in l:
            for k in l:
                m = [Vec3(i,j,k)]
                print i,j,k,'->',[int(h) for h in (t*m)[0]]
    print TransMatrix(t.invT)*[Vec3(0,0,(50**2+30**2+20**2)**.5)]
