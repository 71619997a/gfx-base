from base import Image
from line import line
import triangle
import matrix
import math
from common import *


def edgemtx():
    return [[],[],[],[]]

def addEdgeMtxs(m1, m2):
    m = [m1[i] + m2[i] for i in range(len(m1))]
    return m

def addToEdgeMtx(m, m2):
    for i in range(len(m)):
        m[i] += m2[i]

def addPoint(m, x, y, z):
    m[0].append(x)
    m[1].append(y)
    m[2].append(z)
    m[3].append(1.)

def addEdge(m, x0, y0, z0, x1, y1, z1):
    addPoint(m, x0, y0, z0)
    addPoint(m, x1, y1, z1)

def addEdgesFromParam(m, fx, fy, fz, step):
    t = step
    lastpt = (fx(0), fy(0), fz(0))
    while t <= 1.001:
        pt = (fx(t), fy(t), fz(t))
        addEdge(m, *lastpt + pt)
        lastpt = pt
        t += step

def polyParametrize(poly):
    print poly
    def f(t):
        ret = 0
        for i in range(len(poly)):
            ret += poly[len(poly) - 1 - i] * t ** i
        return ret
    return f

def addCircle(m, cx, cy, cz, r, step):
    def x(t):
        return math.cos(2*math.pi*t)*r + cx
    def y(t):
        return math.sin(2*math.pi*t)*r + cy
    z = lambda t: cz
    addEdgesFromParam(m,x,y,z,step)

    
def addBezier(m, x1, y1, x2, y2, x3, y3, x4, y4, step):
    bezMatrix = [
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ]
    xcoef = matrix.multiply(bezMatrix, matrix.transpose([[x1, x2, x3, x4]]))
    ycoef = matrix.multiply(bezMatrix, matrix.transpose([[y1, y2, y3, y4]]))
    x = polyParametrize(matrix.transpose(xcoef)[0])
    y = polyParametrize(matrix.transpose(ycoef)[0])
    z = lambda t: 0
    addEdgesFromParam(m, x, y, z, step)

def addHermite(m, p0x, p0y, p1x, p1y, m0x, m0y, m1x, m1y, step):
    hermMatrix = [
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ]
    xcoef = matrix.multiply(hermMatrix, matrix.transpose([[p0x, p1x, m0x, m1x]]))
    ycoef = matrix.multiply(hermMatrix, matrix.transpose([[p0y, p1y, m0y, m1y]]))
    x = polyParametrize(matrix.transpose(xcoef)[0])
    y = polyParametrize(matrix.transpose(ycoef)[0])
    z = lambda t: 0
    addEdgesFromParam(m, x, y, z, step)

def linspace(p1, stop=None, step=None):
    if stop is None:
        stop = p1
        start = 0
        step = 1
    elif step is None:
        start = p1
        step = 1
    else:
        start = p1
    i = start
    while i < stop:
        yield i
        i += step
    
def sphere(r, step):
    # theta along base circle, phi up
    # radius of base circ = cos phi
    # height of circ = z = cos phi
    # x = cos theta sin phi
    # y = sin theta sin phi
    # phi from 0 to pi, theta from 0 to 2pi
    tspace = list(linspace(0, 1 + float(step)/2, step))
    sin1 = [math.sin(t * math.pi) for t in tspace]
    sin2 = [math.sin(t * 2*math.pi) for t in tspace]
    cos1 = [math.cos(t * math.pi) for t in tspace]
    cos2 = [math.cos(t * 2*math.pi) for t in tspace]
    points = []
    for theta in tspace:
        points.append(edgemtx())
        for phi in tspace:
            addPoint(points[-1], r*math.sin(phi*math.pi) * math.cos(theta*2*math.pi), r*math.sin(phi*math.pi) * math.sin(theta*2*math.pi), r*math.cos(phi*math.pi))
    tris = edgemtx()
    doublerange = [i for i in range(len(tspace)) for j in range(2)]
    pt_seq = zip([0,1] * len(tspace), doublerange[1:] + [0])
    print pt_seq
    for i in range(len(tspace)):
        rows = [points[i], points[(i + 1) % (len(tspace))]]
        for j in range(len(pt_seq) - 2):
            args = []
            for k in range(j, j + 3):
                for l in range(3):
                    args.append(rows[pt_seq[k][0]][l][pt_seq[k][1]])
            addTriangle(tris, *args)
    return tris


def addTriangle(m, *args):
    assert len(args) == 9
    for i in range(0, 9, 3):
        addPoint(m, *args[i : i+3])

def drawEdges(m, image, color=(0, 0, 0)):  # draws the edges to an image
    for i in range(0, len(m[0]) - 1, 2):
        lin = line(m[0][i], m[1][i], m[0][i + 1], m[1][i + 1])
        coloredlin = [xy + (color,) for xy in lin]
        image.setPixels(coloredlin)

def drawTriangles(m, image, wireframe=False, color=(255, 0, 0), bordercol=(0, 0, 0), hasBorder=True, culling=True):
    triangles = []
    for i in range(0, len(m[0]) - 2, 3):
        triangles.append([m[0][i], m[1][i], m[0][i + 1], m[1][i + 1], m[0][i + 2], m[1][i + 2], m[2][i], m[2][i + 1], m[2][i + 2]])
    ordTris = sorted(triangles, key=lambda l: l[6]+l[7]+l[8])
    for t in ordTris:
        if culling:
            x12 = t[0] - t[2]
            y12 = t[1] - t[3]
            x23 = t[0] - t[4]
            y23 = t[1] - t[5]
            if x12 * y23 - x23 * y12 <= 0:
                continue
        if not wireframe:
            tri = triangle.triangle(*t[:6])
            coloredtri = [xy + (color,) for xy in tri]
        else:
            coloredtri = []
        if hasBorder:
            border = line(*t[:4])
            border.extend(line(*t[2:6]))
            border.extend(line(*t[:2] + t[4:6]))
            coloredtri += [xy + (bordercol,) for xy in border]
            image.setPixels(coloredtri)
    

            
def drawColoredTriangles(ms, image, bordercol=(255, 255, 255)):
    mcols = edgemtx() + [[]]
    for m, col in ms:
        mcol = m + [[col] * len(m[0])]
        mcols = addEdgeMtxs(mcols, mcol)
    triangles = []
    for i in range(0, len(mcols[0]) - 2, 3):
        # print i, mcols[0][i], mcols[1][i], mcols[0][i + 1], mcols[1][i + 1], mcols[0][i + 2], mcols[1][i + 2], sum(mcols[2][i : i+3]), mcols[4][i]
        triangles.append([mcols[0][i], mcols[1][i], mcols[0][i + 1], mcols[1][i + 1], mcols[0][i + 2], mcols[1][i + 2], sum(mcols[2][i : i+3]), mcols[4][i]])
    ordTris = sorted(triangles, key=lambda l: l[6])
    for t in ordTris:
        tri =triangle.triangle(*t[:6])
        border = line(*t[:4])
        border.extend(line(*t[2:6]))
        border.extend(line(*t[:2] + t[4:6]))
        coloredtri = [xy + (t[7],) for xy in tri] + [xy + (bordercol,) for xy in border]
        image.setPixels(coloredtri)
    
        
def mtxTest1():
    m1 = [[2, 2, 3], [3, 2, 2]]
    m2 = [[1, 5], [6.5, 4], [1, -0.7]]
    m3 = [[1, 2, 3, 1], [5, 2, -1, 3], [-1, -5, 3, 6], [2, 4, -7, 2]]
    k1 = 2.5
    k2 = 3.5
    id3 = matrix.id(3)
    id2 = matrix.id(2)
    print 'identity 3x3'
    print matrix.toStr(id3)
    print 'identity 2x2'
    print matrix.toStr(id2)
    print 'm1 2x3'
    print matrix.toStr(m1)
    print 'sanity checks: m1 * id3 = m1, id2 * m1 = m1'
    m1again = matrix.multiply(m1, id3)
    m1evenmore = matrix.multiply(id2, m1)
    print matrix.toStr(m1again)
    print matrix.toStr(m1evenmore)
    print 'testing size mismatch id3 * m1:'
    try:
        matrix.multiply(id3, m1)
    except ArithmeticError:
        print 'it errored, that\'s good'
    print 'm2 3x2'
    print matrix.toStr(m2)
    m12 = matrix.multiply(m1, m2)
    print 'm1 * m2, should be a 2x2'
    print matrix.toStr(m12)
    m21 = matrix.multiply(m2, m1)
    print 'm2 * m1, should be a 3x3'
    print matrix.toStr(m21)
    print '10 * (m2 * m1)'
    print matrix.toStr(matrix.multiply(10, m21))
    print '(m2 * m1) * 10'
    print matrix.toStr(matrix.multiply(m21, 10))
    print '10 * 10'
    print matrix.multiply(10, 10)
    print 'Adding edge (1, 1, 1), (2, 3, 2.5)'
    m = edgemtx()
    addEdge(m, 1, 1, 1, 2, 3, 2.5)
    print matrix.toStr(m)
    print 'm3'
    print matrix.toStr(m3)
    print 'Transforming edge matrix'
    print matrix.toStr(matrix.multiply(m3, m))
    
    img = Image(500, 500)
    for loc in range(0, 500, 4):
        edges = edgemtx()
        addEdge(edges, 125, loc, 100, loc + 1, 375, 100)
        addEdge(edges, loc + 1, 375, 100, 375, 500 - loc - 2, 100)
        addEdge(edges, 375, 500 - loc - 2, 100, 500 - loc - 3, 125, 100)
        addEdge(edges, 500 - loc - 3, 125, 100, 125, loc + 4, 100)
        drawEdges(edges, img, (255 - loc / 2, loc / 2, 127))  # crossfade r + g
    img.display()

def triangleTest1():
    tris = edgemtx()
    img = Image(500, 500)
    for x in range(0, 500, 50):
        for y in range(0, 500, 50):
            addTriangle(tris, x, y, 0, x + 25, y, 0, 250, 250, 250)
    drawTriangles(tris, img)
    img.display()

def circleTest1():
    import math
    m = edgemtx()
    addEdgesFromParam(m, lambda t: 250 + 100 * math.cos(t * 2 * math.pi), lambda t: 250 + 100 * math.sin(t * 2 * math.pi), lambda t: 0, 0.01)
    img = Image(500, 500)
    drawEdges(m, img)
    img.display()

def circleTest2():
    m = edgemtx()
    for theta in range(36):
        costheta = math.cos(theta)
        def fx(t):
            return 250 + 100 * math.cos(t * 2 * math.pi) * costheta
        
if __name__ == '__main__':
    import transform
    
    m = transform.T(250,250,0)*transform.R('x', 30)*transform.R('y', 30)*sphere(200, .05)
    mat = transform.T(250, 250, 0) * transform.R('y', 5) * transform.T(-250, -250, 0)
    for i in range(72):
        img = Image(500,500)
        drawTriangles(m, img)
        m = mat * m
        print i, 'iter'
        img.savePpm('sphere/%d.ppm' % (i))
    

    
