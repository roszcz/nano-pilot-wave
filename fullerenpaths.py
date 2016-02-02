import matplotlib.pyplot as plt
import numpy as np

def read_pos(filepath):
    out = []
    with open(filepath) as fin:
	next(fin)
	for line in fin:
	    vals = line.split()
	    out.append([float(val) for val in vals])

    return out

def show_fullerene():
    """ Show results for fullerene case OBSOLETE """
    apos = read_pos('data/a_fullerene_pos.dat')

    x = [pos[0] for pos in apos]
    y = [pos[1] for pos in apos]
    z = [pos[2] for pos in apos]

    plt.plot(x, y)
    plt.show()
    plt.plot(z)
    plt.show()

def show_single_ball():
    """ Better fixed hexagonal structure with heave bouncer """
    apos = read_pos('data/single_ball.dat')

    t           = [pos[0] for pos in apos]
    z_ball      = [pos[1] for pos in apos]
    z_membrane  = [pos[2] for pos in apos]

    plt.plot(t, z_ball, c='black')
    plt.plot(t, z_membrane, c='green')
    plt.legend(['ball', 'membrane'], loc = 'center right')
    plt.show()

if __name__ == '__main__':
    """ %run this.file.py """
    show_single_ball()
