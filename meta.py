ops = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/'}
def genFsVx(vars):
    l = str(len(vars))
    fs = []
    defn = '    def __%s__(self, o):'
    oth = 'o.%s'
    me = 'self.'
    for op in ['add', 'sub', 'mul', 'div']:
        if op == 'mul':
            oth = 'o'
        for pre in ['i', '']:
            eqin = '=' if pre != '' else ''
            jn = '\n        ' if pre != '' else ','
            stin = 'return Vec'+l+'(%s)' if pre == '' else '%s'
            
            df = defn % (pre+op)
            stlines = []
            for v in vars:
                oexp = oth % (v) if oth != 'o' else oth
                stlines.append(me+v+ops[op]+eqin+oexp)
            fs.append(df+'\n        '+stin % (jn.join(stlines)))
    return '\n\n'.join(fs)

def rewrite(lines):
    new = ''
    i = 0
    for line in lines:
        line = line.strip('\r\n')
        print len(line), line
        line = line.replace('self', 'vec')
        if line[:5] == 'class':
            i = line[9]
            print i
            continue
        ln = line[4:]
        if ln[:3] == 'def':
            if ln[4:6] == '__':
                end = ln.find('_', 6)
                name = ln[6:end]
                oth = ln[end+2:]
            else:
                end = ln.find('(', 4)
                name = ln[4:end]
                oth = ln[end:]
            new += 'def ' + name + i + oth
        else:
            new += ln
        new += '\n'
    return new

with open('vector.py') as f:
    print rewrite(f.readlines())
