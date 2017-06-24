from line import lineByY, line
#import transform
#from matrix import multiply
#import matrix
#from os import chdir
#from multiprocessing import Pool
#from png import Reader
#from time import time
#from base import Image
#import obj
#import edgeMtx
import math
from common import *

#chdir('/storage/emulated/0/qpython/scripts/gfx-base/gfx-base')


# def sortedInds(lst):
#     fix = enumerate(lst)
#     sort = sorted(fix, key=lambda t: t[1])
#     return tuple(zip(*sort)[::-1])

# def inOrder(lst, order):
#     return [lst[i] for i in order]

# def topTriangle(yBase, x1Base, x2Base, x1Top, y1Top):
#     pts = []
#     if x1Base > x1Top:
#         border1 = lineByY(x1Base, yBase, x1Top, y1Top)
#     else:
#         border1 = lineByY(x1Base, yBase, x1Top, y1Top)[::-1]
#     if x2Base > x1Top:
#         border2 = lineByY(x2Base, yBase, x1Top, y1Top)
#     else:
#         border2 = lineByY(x2Base, yBase, x1Top, y1Top)[::-1]
#     i = 0
#     for y in range(int(math.ceil(y1Top)), int(math.ceil(yBase))):
#         try:
#             border1[i][0]
#             border2[i][0]
#         except IndexError:
#             continue
#         for x in range(border1[i][0], border2[i][0]+1):
#             pts.append((x, y))
        
#         i += 1
#     return pts + border1 + border2

# def botTriangle(yBase, x1Base, x2Base, x1Bot, y1Bot):
#     pts = []
#     if x1Base > x1Bot:
#         border1 = lineByY(x1Base, yBase, x1Bot, y1Bot)[::-1]
#     else:
#         border1 = lineByY(x1Base, yBase, x1Bot, y1Bot)
#     if x2Base > x1Bot:
#         border2 = lineByY(x2Base, yBase, x1Bot, y1Bot)[::-1]
#     else:
#         border2 = lineByY(x2Base, yBase, x1Bot, y1Bot)
#     i = 0
#     for y in range(int(math.ceil(yBase)), int(math.ceil(y1Bot + 1))):
#         try:
#             border1[i][0]
#             border2[i][0]
#         except IndexError:
#             continue
#         for x in range(border1[i][0], border2[i][0]+1):
#             pts.append((x, y))
#         i += 1
#     return pts + border1 + border2


PREC = 20
PRMUL = 1 << PREC
def triangle(x1, y1, x2, y2, x3, y3):
    if x1 == 225 or x2 == 225 or x3 == 225:
        print x3 - x1, x2 - x1, x3 - x2
    pts = []
    # 1. floating point -> fixed point
    x1 = int(round(x1 * PRMUL))  # integer + n bytes of fixed prec
    x2 = int(round(x2 * PRMUL))
    x3 = int(round(x3 * PRMUL))
    y1 = int(round(y1 * PRMUL))
    y2 = int(round(y2 * PRMUL))
    y3 = int(round(y3 * PRMUL))

    # 2. find bounding box
    yMin = (min(y1, y2, y3) + PRMUL - 1) >> PREC  # integer, +2^n-1 b/c rounding
    yMax = (max(y1, y2, y3) + PRMUL - 1) >> PREC  
    xMin = (min(x1, x2, x3) + PRMUL - 1) >> PREC
    xMax = (max(x1, x2, x3) + PRMUL - 1) >> PREC
    if yMax > 500 and yMin < 0 and xMin < 0 and xMax > 500:
        print 'large triangle detected:'
        print x1, y1, x2, y2, x3, y3
        return []
    # 3. use eq of line to find interior:
    # on line if (y - y1)(x1 - x2) - (x - x1)(y1 - y2) = 0
    # y(x1 - x2) - x(y1 - y2) + C = 0
    # increment y = x1 - x2
    # incr3ement x = y2 - y1
    # C = x1(y1 - y2)-y1(x1 - x2)
    # only fill left & flat top edges (by convention), so inc c if we have one
    x12 = x1 - x2  # integer + n bytes of fixed prec
    y12 = y1 - y2
    x23 = x2 - x3
    y23 = y2 - y3
    x31 = x3 - x1
    y31 = y3 - y1
    fx12 = x12 << PREC  # integer + 2n bytes of fixed prec
    fy12 = y12 << PREC
    fx23 = x23 << PREC
    fy23 = y23 << PREC
    fx31 = x31 << PREC
    fy31 = y31 << PREC
    c12 = x1*y12-y1*x12  # integer + 2n bytes of fixed prec
    c23 = x2*y23-y2*x23
    c31 = x3*y31-y3*x31
    if y12 < 0 or (y12 == 0 and x12 > 0):
        c12 += 2
    if y12 < 0 or (y23 == 0 and x23 > 0):
        c23 += 2
    if y31 < 0 or (y31 == 0 and x31 > 0):
        c31 += 2
    x = xMin
    y = yMin
    fx = x << PREC
    fy = y << PREC
    A12start = fy*x12 - fx*y12 + c12  # integer + 2n bytes of fixed prec
    A23start = fy*x23 - fx*y23 + c23
    A31start = fy*x31 - fx*y31 + c31
    #print A12start, A23start, A31start
    # 4. Loop
    xr = xrange(xMin, xMax)
    for y in xrange(yMin, yMax):
        # start at x=xmin, y=whatever
        A12 = A12start
        A23 = A23start
        A31 = A31start
        hbin=False
        for x in xr:
            if A12 > 0 and A23 > 0 and A31 > 0:
                pts.append((x, y))
                hbin=True
            elif hbin:
                break
            A12 -= fy12
            A23 -= fy23
            A31 -= fy31
            #print A12, A23, A31
        # discard A, move Astart down
        A12start += fx12
        A23start += fx23
        A31start += fx31
    return pts
            
if __name__ == '__main__':
    pass

