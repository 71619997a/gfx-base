def getcolumn(arr2d, idx):
        col = []
        for row in arr2d:
                col.append(row[idx])
        return col
        
def transpose(m):
        return [getcolumn(m, i) for i in range(len(m[0]))]

def multiply(fac1, fac2):  # chooses between matrix or scalar multiplication
        try:
                a = fac1[0]
                f1scalar = False
        except TypeError:
                f1scalar = True

        try:
                a = fac2[0]
                f2scalar = False
        except TypeError:
                f2scalar = True

        if f1scalar:
                if f2scalar:  # easy case
                        return fac1 * fac2
                else:  # k1 * m2
                        return scalarMult(fac2, fac1)
        else:
                if f2scalar:  # m1 * k2
                        return scalarMult(fac1, fac2)
                else:  # matrix mult
                        return mtxMult(fac1, fac2)

def mtxMult(m1, m2):
        if len(m1[0]) != len(m2):
                raise ArithmeticError("Size mismatch in matrices: %dx%d * %dx%d"%(len(m1[0]),len(m1),len(m2[0]),len(m2)))
        m2t = transpose(m2)
        mret = []
        for row in m1:
                mret.append([])
                for i in range(len(m2t)):
                        col = m2t[i]
                        dot = 0
                        for j in range(len(row)):
                                dot += col[j] * row[j]
                        mret[-1].append(dot)
        return mret


def scalarMult(m, k):
        return [[k * i for i in j] for j in m]

def id(n):
        return [[0 if i != j else 1 for i in range(n)] for j in range(n)]

def toStr(m):
        ret = '[\n'
        for row in m:
                ret += '\t'
                for n in row:
                        ret += "{:7.2f}  ".format(n)  # width of 7, 2 decimal prec
                ret += '\n'
        return ret + ']'
