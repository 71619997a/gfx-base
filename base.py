from random import randint, random
import math
import os
import re
import matrix
from time import time
WIDTH = 500
HEIGHT = 500

rgbStrTable = [str(i) for i in range(256)]
class Image(object):
        def __init__(self, w, h, pix=None):
                if pix is None:
                        self.pixels = [[(255,255,255) for _ in xrange(w)] for __ in xrange(h)]
                else:
                        self.pixels = pix
                self.width = w
                self.height = h

        def savePpm(self, name):
                header = 'P6 %d %d 255\n' % (self.width, self.height)
                ba = bytearray([c for row in self.pixels for rgb in row for c in rgb])
                # for row in self.pixels:
                #         for rgb in row:
                #                 ba.extend(rgb)
                with open(name, 'wb') as f:
                        f.write(header)
                        f.write(ba)
                # with open(name, 'w') as f:
                #         f.write('P3 %d %d 255\n' % (self.width, self.height))
                #         for row in self.pixels:
                #                 for rgb in row:
                #                         f.write('%d %d %d ' % tuple(rgb))
                #                 f.write('\n')


        def saveAs(self, name):
                self.savePpm('temp.ppm')
                os.system('convert temp.ppm ' + name)
                os.system('rm temp.ppm')

        def display(self):  # displays image and deletes after
                self.savePpm('temp.ppm')
                os.system('display temp.ppm')
                os.system('rm temp.ppm')

        def setPixel(self, x, y, col):
                if x >= 0 and y >= 0:  # no wraparound pls
                        try:
                                self.pixels[y][x] = col
                        except:  # too big
                                return

        def setPixels(self, ls):  # list of (x, y, color)
                for x, y, col in ls:
                        self.setPixel(x, y, col)

        def fromFunc(self, func):
                for y in xrange(self.height):
                        for x in xrange(self.width):
                                setPixel(x, y, func(x, y))

        def flipUD(self):
                return Image(self.width, self.height, self.pixels[::-1])

        @staticmethod
        def fromImage(filename):  # use as img = Image.fromImage(...)
                with open(filename) as f:
                        body = f.read()
                words = filter(None, re.split('[ \n\t]+', body))
                assert words[0] == 'P3'
                vals = [int(i) for i in words[1:]]
                assert len(vals) % 3 == 0
                width = int(vals[0])
                height = int(vals[1])
                img = Image(width, height)
                maxcol = int(vals[2])
                if not maxcol == 255:
                        scalefac = 255. / maxcol
                        vals = [int(i * scalefac) for i in vals]
                for i in range(3, len(vals), 3):
                        s3 = i / 3 - 1
                        rgb = tuple(vals[i : i+3])
                        img.setPixel(s3 % width, s3 / width, rgb)
                return img

def makeAnimation(name, format='png'):
        os.system('convert -delay 5 anim/%s*.%s %s.gif' % (name, format, name))

def clearAnim():
        os.system('rm anim/*')

def animate(name):
        os.system('animate %s.gif' % (name))
