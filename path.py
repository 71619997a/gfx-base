from common import *

def _lerp(s, e, l):
    return s * (1-l) + e * l
def addPathAct(path, act):
    path.extend(act)
    print len(path)
    path.extend([act[-1]] * 15)


def addPathMove(path, camPStart, camPEnd, camUStart, camUEnd, lookStart, lookEnd, frames):
    act = []
    for i in range(frames):
        lerpFac = float(i) / (frames - 1)
        P = [_lerp(camPStart[j], camPEnd[j], lerpFac) for j in range(3)]
        U = [_lerp(camUStart[j], camUEnd[j], lerpFac) for j in range(3)]
        cam = Camera(*P+U)
        L = [_lerp(lookStart[j], lookEnd[j], lerpFac) for j in range(3)]
        act.append((cam, L))
    addPathAct(path, act)
    return act

def addPlanetCircle(path, camPStart, look, rad, frames):
    def getP(t):
        ang = t * 2 * math.pi
        return [camPStart[0] - rad + rad * math.cos(ang), camPStart[1] + rad*math.sin(ang), camPStart[2]]
    act = []
    for i in range(frames):
        t = float(i) / (frames - 1)
        cam = Camera(*getP(t) + [0,0,1])
        act.append((cam, look))
    addPathAct(path, act)
    return act

if __name__ == '__main__':
    path = []
    addPlanetCircle(path, [100, 0, 2111], [1,1,1], 100, 50)
    for cam, L in path:
        print cam.x, cam.y, cam.z, cam.ux, cam.uy, cam.uz
