import math
from base import Image
from sys import argv

def _r(x):
    return int(x)

def line(x0, y0, x1, y1):
    x0, y0, x1, y1 = _r(x0), _r(y0), _r(x1), _r(y1)
    if x0 > x1:  # 
        x0, x1, y0, y1 = x1, x0, y1, y0
    if y0 < y1:  # q1
        if y1 - y0 > x1 - x0:  # o2
            return line2(x0, y0, x1, y1)
        return line1(x0, y0, x1, y1)  # o1
    # q4
    if y0 - y1 > x1 - x0:  # o7
        return line7(x0, y0, x1, y1)
    return line8(x0, y0, x1, y1)

def lineByY(x0, y0, x1, y1):
    x0, y0, x1, y1 = _r(x0), _r(y0), _r(x1), _r(y1)
    if x0 > x1:  # 
        x0, x1, y0, y1 = x1, x0, y1, y0
    if y0 < y1:  # q1
        return line1Y(x0, y0, x1, y1)  # o1
    elif y0 > y1:
        return line8Y(x0, y0, x1, y1)
    else:
        return [(x0, y0)]

def line1(x0, y0, x1, y1):
    pts = []
    x = x0
    y = y0
    a = 2 * (y1 - y0)
    b = x0 - x1
    d = a + b
    b *= 2
    while x <= x1:
        pts.append((x, y))
        if d > 0:
            y += 1
            d += b
        x += 1
        d += a
    return pts

def line1Y(x0, y0, x1, y1):
    pts = []
    x = _r(x0)
    y = _r(y0)
    a = y1 - y0
    b = 2 * (x0 - x1)
    d = a + b
    a *= 2
    while y <= y1:
        pts.append((x, y))
        while d < 0:
            x += 1
            d += a
        y += 1
        d += b
    return pts

def line2(x0, y0, x1, y1):
    pts = []
    x = x0
    y = y0
    a = y1 - y0
    b = 2 * (x0 - x1)
    d = a + b
    a *= 2
    while y <= y1:
        pts.append((x, y))
        if d < 0:
            x += 1
            d += a
        y += 1
        d += b
    return pts

def line7(x0, y0, x1, y1):
    pts = []
    x = x0
    y = y0
    a = y1 - y0
    b = 2 * (x0 - x1)
    d = a - b
    a *= 2
    while y >= y1:
        pts.append((x, y))
        if d > 0:
            x += 1
            d += a
        y -= 1
        d -= b
    return pts

def line8Y(x0, y0, x1, y1):
    pts = []
    x = _r(x0)
    y = _r(y0)
    a = y1 - y0
    b = 2 * (x0 - x1)
    d = a - b
    a *= 2
    while y >= y1:
        pts.append((x, y))
        while d > 0:
            x += 1
            d += a
        y -= 1
        d -= b
    return pts

def line8(x0, y0, x1, y1):
    pts = []
    x = x0
    y = y0
    a = 2 * (y1 - y0)
    b = x0 - x1
    d = a - b
    b *= 2
    while x <= x1:
        pts.append((x, y))
        if d < 0:
            y -= 1
            d -= b
        x += 1
        d += a
    return pts

if __name__ == '__main__': 
    print 'Running line test'
    img = Image(500, 500)
    xys = [(125, 0), (375, 0), (0, 125), (0, 375), (500, 125), (500, 375), (125, 500), (375, 500), (500, 500), (0, 0), (250, 0), (0, 250), (250, 500), (500, 250), (0, 500), (500, 0)]
    pts = [pt for coords in xys for pt in lineByY(250, 250, *coords)]
    for pt in pts:
        if 500 > pt[0] >= 0 and 500 > pt[1] >= 0:
            img.setPixel(pt[0], 499 - pt[1], (255,0,0))

    img.display()
