from edgeMtx import edgemtx, addToEdgeMtx, addTriangle, addPoint, addEdge, addCircle, drawEdges
import math
import transform
from common import *

def genBoxPoints(x, y, z, w, h, d):
    # how to preserve orientation for dummies
    if w < 0:
        return genBoxPoints(x + w, y, z, -w, h, d)
    if h < 0:
        return genBoxPoints(x, y - h, z, w, -h, d)
    if d < 0:
        return genBoxPoints(x, y, z - d, w, h, -d)
    pts = []
    for i in range(8):
        xcor = x + (i >> 2) * w
        ycor = y - (i >> 1) % 2 * h
        zcor = z - d + i % 2 * d
        pts.append((xcor, ycor, zcor))
    return pts

def genBoxTris():
    return [(0, 1, 5), (0, 5, 4), (2, 7, 3), (2, 6, 7), (0, 6, 2), (0, 4, 6), (1, 3, 7), (1, 7, 5), (0, 3, 1), (0, 2, 3), (4, 5, 7), (4, 7, 6)]

def addBox(m, x, y, z, w, h, d):
    pts = genBoxPoints(x, y, z, w, h, d)
    for a,b,c in genBoxTris():
        addTriangle(m, *pts[a]+pts[b]+pts[c])

def addSphere(m, x, y, z, r, step=0.02):
    pts = genSpherePoints(x, y, z, r, step)
    tris = genSphereTris(step)
    fixOverlaps(pts, tris)
    for a,b,c in tris:
        addTriangle(m, *pts[a]+pts[b]+pts[c])

def fixOverlaps(pts, tris, thresh=15):
    fac = 2 ** thresh
    origs = {}
    reals = {}
    for i in range(len(pts)):
        pt = pts[i]
        x = int(pt[0] * fac)
        y = int(pt[1] * fac)
        z = int(pt[2] * fac)
        if (x, y, z) in origs:
            reals[i] = origs[(x, y, z)]
            # print 'OVERLAP -----'
            # print 'Original point: #%d at ' % (reals[i]) + str(pts[reals[i]])
            # print 'This point: #%d at ' % (i) + str(pts[i])
        else:
            origs[(x, y, z)] = i
            reals[i] = i
    for i in range(len(tris)):
        tris[i] = tuple(reals[j] for j in tris[i])

def genSphereTris(step=0.02):
    tris = []
    steps = int(math.ceil(1 / step))
    for i in range(steps):
        for j in range(steps - 1):
            iNext = (i + 1) % steps
            jNext = (j + 1) % steps
            cor = i * steps + j
            leftcor = i * steps + jNext
            topcor = iNext * steps + j
            diagcor = iNext * steps + jNext
            tris.append((cor, diagcor, leftcor))
            tris.append((cor, topcor, diagcor))
    return tris

def checkOrient(p1, p2, p3):
    pass

def genSpherePoints(x, y, z, r, step=0.02):
    pts = []
    steps = int(math.ceil(1 / step))
    theps = 0
    thep = 2 * math.pi / steps
    phep = math.pi / (steps - 1)
    for theta in range(steps):
        pheps = 0
        for phi in range(steps):
            xcor = x + r * math.sin(pheps) * math.cos(theps)
            ycor = y + r * math.sin(pheps) * math.sin(theps)
            zcor = z + r * math.cos(pheps)
            pts.append((xcor, ycor, zcor))
            pheps += phep
        theps += thep
    return pts

def addTorus(m, x, y, z, r, R, mainStep=0.02, ringStep=0.05):
    pts = genTorusPoints(x, y, z, r, R, mainStep, ringStep)
    for a,b,c in genTorusTris(mainStep, ringStep):
        addTriangle(m, *pts[a]+pts[b]+pts[c])

def genTorusTris(mainStep=0.02, ringStep=0.05):
    steps = int(math.ceil(1 / mainStep))
    rsteps = int(math.ceil(1 / ringStep))
    tris = []
    for c in range(steps):
        for r in range(rsteps):
            cNext = (c + 1) % steps
            rNext = (r + 1) % rsteps
            cor = c * rsteps + r
            rightcor = c * rsteps + rNext
            topcor = cNext * rsteps + r
            diagcor = cNext * rsteps + rNext
            tris.append((cor, rightcor, diagcor))
            tris.append((cor, diagcor, topcor))
    return tris

            

def genTorusPoints(x, y, z, r, R, mainStep=0.02, ringStep=0.05):
    pts = []
    steps = int(math.ceil(1 / mainStep))
    rsteps = int(math.ceil(1 / ringStep))
    om = 2 * math.pi / steps
    im = 2 * math.pi / rsteps
    for theta in range(steps):
        for phi in range(rsteps):
            xcor = math.cos(theta * om) * (r * math.cos(phi * im) + R) + x
            ycor = r * math.sin(phi * im) + y
            zcor = -math.sin(theta * om) * (r * math.cos(phi * im) + R) + z
            pts.append((xcor, ycor, zcor))
    return pts

        
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    def addIP(a, v):
        for i in xrange(len(v)):
            a[i] += v[i]

    def genVertexNorms(vxs, tris):
        norms = [[0,0,0] for _ in vxs]
        for p1, p2, p3 in tris:
            an1, an2, an3 = norms[p1], norms[p2], norms[p3]
            v1, v2, v3 = vxs[p1], vxs[p2], vxs[p3]
            v12x, v12y, v12z = tuple(v2[n]-v1[n] for n in range(3))
            v23x, v23y, v23z = tuple(v3[n]-v2[n] for n in range(3))
            v31x, v31y, v31z = tuple(v1[n]-v3[n] for n in range(3))
            try:
                c1 = cross(v31x, v31y, v31z, -v12x, -v12y, -v12z)
                c2 = cross(v12x, v12y, v12z, -v23x, -v23y, -v23z)
                c3 = cross(v23x, v23y, v23z, -v31x, -v31y, -v31z)
            except ZeroDivisionError:
                continue
            addIP(an1, c1)
            addIP(an2, c2)
            addIP(an3, c3)
        for i in range(len(norms)):
            n = norms[i]
            if n != [0.,0.,0.]:
                norms[i] = normalizedTuple(n)
            else:
                norms[i] = (1.,0.,0.)
        return norms

    def genTCs(norms):
        return [(0.5 + math.atan2(-n[2], -n[0])/math.pi/2, 0.5 - math.asin(-n[1])/math.pi) for n in norms]


    def getPointsFromTriangles(m):  # assumes m is a poly mtx
        for i in range(0, len(m[0]), 3):
            v12x, v12y, v12z = tuple(m[n][i] - m[n][i+1] for n in range(3))
            v23x, v23y, v23z = tuple(m[n][i+1] - m[n][i+2] for n in range(3))
            v31x, v31y, v31z = tuple(m[n][i+2] - m[n][i] for n in range(3))
            try:
                n1 = normalizeList(cross(-v31x, -v31y, -v31z, v12x, v12y, v12z))
                n2 = normalizeList(cross(-v12x, -v12y, -v12z, v23x, v23y, v23z))
                n3 = normalizeList(cross(-v23x, -v23y, -v23z, v31x, v31y, v31z))
            except ZeroDivisionError:
                continue
            yield (Point(m[0][i], m[1][i], m[2][i], n1[0], n1[1], n1[2], 0, 0),
                   Point(m[0][i+1], m[1][i+1], m[2][i+1], n2[0], n2[1], n2[2], 0, 0),
                   Point(m[0][i+2], m[1][i+2], m[2][i+2], n3[0], n3[1], n3[2], 0, 0))

    def trianglesFromVTNT(vxs, tris, norms=None, tcs=None):
        if norms is None:
            norms = genVertexNorms(vxs, tris)
        if tcs is None:
            tcs = genTCs(norms)
        for a,b,c in tris:
            yield (
                Point(*vxs[a]+norms[a]+tcs[a]),
                Point(*vxs[b]+norms[b]+tcs[b]),
                Point(*vxs[c]+norms[c]+tcs[c]))

    tris = genSphereTris(0.05)
    vxs = genSpherePoints(0,0,0,100,0.05)
    fixOverlaps(vxs, tris)
    pts = list(trianglesFromVTNT(vxs, tris))
    tcs = [(p.tx, p.ty) for t in pts for p in t]
    tcs = zip(*sorted(tcs, key=lambda a:a[0]))
    plt.plot(*tcs+['ro'])
    plt.show()
    print tcs