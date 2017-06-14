from os import system
from sys import argv


if __name__ == '__main__':
    if len(argv) < 2:
        print 'Usage: python blockit.py <mdl> [N]'
        exit(1)
    elif len(argv) < 3:
        print 'N not specified, defaulting to 150...'
        fil = argv[1]
        N = 150
    else:
        fil = argv[1]
        N = int(argv[2])
    for i in range(0, 771, N):
        system('python script.py %s %i %i' % (fil, i, N))
