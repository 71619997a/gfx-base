import mdl
from transform import TransMatrix
import transform
from edgeMtx import edgemtx, addEdge, addTriangle, drawEdges, addBezier, addHermite, addCircle, drawTriangles
from base import Image, makeAnimation, clearAnim
from render import renderTriangle, phongShader, drawObjectsNicely, drawObjects, autoTrianglesFromVT, flatTrisFromVT, trianglesFromVTNT
import render
import shape
from sys import argv
import time
from common import *


EDGE = 2
POLY = 3
ka = kd = Texture(True, (0,0,0), 'jupiter.png')
ks = Texture(False, (30, 30, 10))
mat = Material(ka, kd, ks, 4)

def err(s):
    print 'ERROR\n'+s
    exit(1)

def warn(s):
    print 'Warning\n'+s


def runFrame(frame, commands):
    step = 0.02
    cstack = [TransMatrix()]
    img = Image(500, 500)
    objects = []
    for command in commands:
        inp = command[0]
        args = command[1:]
        if inp == 'line':
            edges = edgemtx()
            addEdge(edges, *command[1:7])
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'ident':
            cstack[-1] = TransMatrix()
        elif inp == 'scale':
            kval = frame[args[3]]
            cstack[-1] *= transform.S(*args[:3]) * transform.S(kval, kval, kval)  # scaling a scale with scale
        elif inp == 'move':
            kval = frame[args[3]]
            cstack[-1] *= transform.T(*[i * kval for i in args[:3]])
        elif inp == 'rotate':
            kval = frame[args[2]]
            cstack[-1] *= transform.R(args[0], args[1] * kval)
        elif inp == 'circle':
            edges = edgemtx()
            addCircle(*(edges,)+command[1:5]+(.01,))
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'bezier':
            edges = edgemtx()
            addBezier(*(edges,)+command[1:9]+(.01,))
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'hermite':
            edges = edgemtx()
            addHermite(*(edges,)+command[1:9]+(.01,))
            edges = cstack[-1] * edges
            objects.append((EDGE, edges))
            #drawEdges(cstack[-1] * edges, img)
        elif inp == 'clearstack':
            cstack = [TransMatrix()]
        elif inp == 'box':
            vxs = cstack[-1] * shape.genBoxPoints(*command[1:7])
            tris = shape.genBoxTris()
            shape.fixOverlaps(vxs, tris)
            objects.append((POLY, flatTrisFromVT(vxs, tris)))
            #polys = edgemtx()
            #shape.addBox(*(polys,) + command[1:7])
            #polys = cstack[-1] * polys
            #objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'sphere':
            vxs = shape.genSpherePoints(*command[1:5]+(step,))
            tris = shape.genSphereTris(step)
            shape.fixOverlaps(vxs, tris)
            pts = trianglesFromVTNT(vxs, tris)
            cstack[-1]*pts
            objects.append((POLY, pts))
            #polys = edgemtx()
            #shape.addSphere(*(polys,) + command[1:5] + (.05,))
            #polys = cstack[-1] * polys
            #objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'torus':
            vxs = cstack[-1] * shape.genTorusPoints(*command[1:6]+(step,step))
            tris = shape.genTorusTris(step,step)
            shape.fixOverlaps(vxs, tris)
            objects.append((POLY, autoTrianglesFromVT(vxs, tris)))
            #polys = edgemtx()
            #shape.addTorus(*(polys,) + command[1:6] + (.05, .05))
            #polys = cstack[-1] * polys
            #objects.append((POLY, polys))
            #drawTriangles(cstack[-1] * polys, img, wireframe=True)
        elif inp == 'push':
            cstack.append(cstack[-1].clone())
        elif inp == 'pop':
            cstack.pop()
    return objects


def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = TransMatrix()

    p = mdl.parseFile(filename)
    #print p
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    frames = None
    basename = 'anim'
    varying = False
    # pass 1
    for command in commands:
        cmd = command[0]
        args = command[1:]
        if cmd == 'frames':
            frames = args[0]
        elif cmd == 'basename':
            basename = args[0]
        elif cmd == 'vary':
            varying = True

    if varying:
        if frames is None:
            err('Frames not set.')
        if basename == 'anim':
            warn('Basename not set, using default of anim.')
        # pass 2
        upd = lambda d, n: 0 if d.update(n) else d
        frameList = [upd({k: v[1] for k, v in symbols.iteritems() if v[0] == 'knob'}, {None: 1}) for _ in range(frames)]
        for command in commands:
            cmd = command[0]
            args = command[1:]
            if cmd == 'set':
                for frame in frameList:
                    frame[args[0]] = args[1]
            elif cmd == 'setall':
                for frame in frameList:
                    for key in frame.keys():
                        frame[key] = args[0]
            elif cmd == 'vary':
                val = args[3]
                inc = (1.*args[4] - args[3])/(args[2] - args[1])
                for frid in range(args[1], args[2] + 1):
                    frameList[frid][args[0]] = val
                    val += inc
        imgs = []
        # pass for each frame
        print 'Pass 2 complete, beginning image rendering...'
        a = time.time()
        tc = {}
        draw = lambda *t: drawObjectsNicely(*t, shader=phongShader, mat=mat, texcache=tc)
        i = 0
        for frame in frameList:
            print 'Rendering frame %d...'%(i)
            objects = runFrame(frame, commands)
            img = Image(500, 500)
            draw(objects, img)
            imgs.append(img)
            i += 1
        print 'Images rendered in %f ms' % (int((time.time() - a) * 1000000)/1000.)
        print 'Saving images...'
        a = time.time()
        for i in range(len(imgs)):
            imgs[i].savePpm('anim/%s%03d.ppm' % (basename, i))
        print 'Images saved in %f ms' % (int((time.time() - a) * 1000000)/1000.)
        print 'Creating animation... (converting to gif)'
        a = time.time()
        makeAnimation(basename, 'ppm')
        print 'Animation created in %f ms' % (int((time.time() - a) * 1000000)/1000.)
        # clearAnim()


    else:
        cstack = [TransMatrix()]
        frc = 0
        img = Image(500, 500)
        objects = []
        for command in commands:
            inp = command[0]
            if inp == 'line':
                edges = edgemtx()
                addEdge(edges, *command[1:7])
                edges = cstack[-1] * edges
                objects.append((EDGE, edges))
                #drawEdges(cstack[-1] * edges, img)
            elif inp == 'ident':
                cstack[-1] = TransMatrix()
            elif inp == 'scale':
                cstack[-1] *= transform.S(*command[1:4])
            elif inp == 'move':
                cstack[-1] *= transform.T(*command[1:4])
            elif inp == 'rotate':
                cstack[-1] *= transform.R(*command[1:3])
            elif inp == 'display':
                drawObjects(objects, img)
                img.flipUD().display()
            elif inp == 'save':
                drawObjects(objects, img)
                if inp[-4:] == '.ppm':
                    img.flipUD().savePpm(command[1])
                else:
                    img.flipUD().saveAs(command[1])
            elif inp == 'saveframe':
                drawObjects(objects, img)
                img.flipUD().savePpm('%s%d.ppm' % (command[1], frc))
                frc += 1
            elif inp == 'circle':
                edges = edgemtx()
                addCircle(*(edges,)+command[1:5]+(.01,))
                edges = cstack[-1] * edges
                objects.append((EDGE, edges))
                #drawEdges(cstack[-1] * edges, img)
            elif inp == 'bezier':
                edges = edgemtx()
                addBezier(*(edges,)+command[1:9]+(.01,))
                edges = cstack[-1] * edges
                objects.append((EDGE, edges))
                #drawEdges(cstack[-1] * edges, img)
            elif inp == 'hermite':
                edges = edgemtx()
                addHermite(*(edges,)+command[1:9]+(.01,))
                edges = cstack[-1] * edges
                objects.append((EDGE, edges))
                #drawEdges(cstack[-1] * edges, img)
            elif inp == 'clear':
                img = Image(500, 500)
            elif inp == 'clearstack':
                cstack = [TransMatrix()]
            elif inp == 'box':
                polys = edgemtx()
                shape.addBox(*(polys,) + command[1:7])
                polys = cstack[-1] * polys
                objects.append((POLY, polys))
                #drawTriangles(cstack[-1] * polys, img, wireframe=True)
            elif inp == 'sphere':
                polys = edgemtx()
                shape.addSphere(*(polys,) + command[1:5] + (.05,))
                polys = cstack[-1] * polys
                objects.append((POLY, polys))
                #drawTriangles(cstack[-1] * polys, img, wireframe=True)
            elif inp == 'torus':
                polys = edgemtx()
                shape.addTorus(*(polys,) + command[1:6] + (.05, .05))
                polys = cstack[-1] * polys
                objects.append((POLY, polys))
                #drawTriangles(cstack[-1] * polys, img, wireframe=True)
            elif inp == 'push':
                cstack.append(cstack[-1].clone())
            elif inp == 'pop':
                cstack.pop()


if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception('\nUsage: python script.py [mdl file]')
    run(argv[1])
