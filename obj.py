from common import *

def parse(objfile, mtlfile):
    from edgeMtx import edgemtx, addTriangle
    with open(mtlfile) as f:
        mtllines = f.readlines()
    materialNext = ''
    materials = {}
    for line in mtllines:
        if line[:7] == 'newmtl ':
            materialNext = line[7:].strip()
        elif line[:4] == '\tKa ':
            color = tuple(int(float(i) * 255) for i in line[4:].strip().split(' '))
            materials[materialNext].amb = Texture(False, color, 0)
        elif line[:4] == '\tKd ':
            color = tuple(int(float(i) * 255) for i in line[4:].strip().split(' '))
            materials[materialNext].diff = Texture(False, color, 0)
        elif line[:4] == '\tKs ':
            color = tuple(int(float(i) * 255) for i in line[4:].strip().split(' '))
            materials[materialNext].spec = Texture(False, color, 0)
        elif line[:4] == '\tNs ':
            exp = float(line[4:].strip())
            materials[materialNext] = Material(0, 0, 0, exp)
        elif line[:8] == '\tmap_Kd ':
            materials[materialNext].diff.texture = line[8:].strip()
            materials[materialNext].diff.type = True
        elif line[:8] == '\tmap_Ka ':
            materials[materialNext].amb.texture = line[8:].strip()
            materials[materialNext].amb.type = True
    vertices = []
    tcors = []
    norms = []
    triangles = []
    colors = []
    mtl = ''
    with open(objfile) as f:
        r = f.readlines()
    for line in r:
        if line[:3] == 'v  ':
            coords = tuple(float(i) for i in line[3:].strip().split(' '))
            vertices.append(coords)
        elif line[:3] == 'vt ':
            coords = tuple(float(i) for i in line[3:].strip().split(' '))[:2]
            tcors.append(coords)
        elif line[:3] == 'vn ':
            coords = tuple(float(i) for i in line[3:].strip().split(' '))
            norms.append(coords)
        elif line[:2] == 'f ':
            if not obj == 'Hair_Cap':
                indices = tuple(int(i.split('/')[0]) for i in line[2:].strip().split(' '))
                tindices = tuple(int(i.split('/')[1]) for i in line[2:].strip().split(' '))
                nindices = tuple(int(i.split('/')[2]) for i in line[2:].strip().split(' '))
                triangles.append((indices,tindices,nindices))
        elif line[:7] == 'usemtl ':
            mtl = line[7:].strip()
            mat = materials[mtl]
            colors.append((len(triangles), mat))
        elif line[:2] == 'g ':
            obj = line[2:].strip()
    triset = []
    for i in range(len(colors)):
        start, mat = colors[i]
        if i + 1 < len(colors):
            end = colors[i + 1][0]
            thiscol = triangles[start:end]
        else:
            thiscol = triangles[start:]
        for ind, tind, nind in thiscol:
            ls = []
            i,j,k = ind
            x,y,z = tind
            a,b,c = nind
            # TODO use Point and Material
            p = Point(*vertices[i - 1] + norms[\
a - 1] + tcors[x - 1])
            ls.append(Point(*vertices[i - 1] + norms[a - 1] + tcors[x - 1]))
            ls.append(Point(*vertices[j - 1] + norms[b - 1] + tcors[y - 1]))
            ls.append(Point(*vertices[k - 1] + norms[c - 1] + tcors[z - 1]))
            ls.append(mat)
            triset.append(ls)
    return triset
