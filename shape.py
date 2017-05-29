from edgeMtx import edgemtx, addToEdgeMtx, addTriangle, addPoint, addEdge, addCircle, drawEdges
import math
import transform

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
    tris = genSphereTris(0.02)
    pts = genSpherePoints(0,0,0,100,0.02)
    fixOverlaps(pts, tris, 15)
