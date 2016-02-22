import matplotlib.pyplot as plt
import numpy as np

def make_position_histogram(filepath, cmap='bone'):
    """ Choosing proper number of bins is important, apparently"""
    # Read the full path from 'data/single_ball.dat'
    scores = read_pos(filepath)
    xx = [pos[2] for pos in scores]
    yy = [pos[3] for pos in scores]

    # Number of bins is defined here by the suqare of number of measurements
    xedges = np.linspace(min(xx), max(xx), np.sqrt(len(xx)))
    yedges = xedges

    # 
    H, xedges, yedges = np.histogram2d(xx, yy, bins=(xedges, yedges))

    # Scale the colors with vmax
    im = plt.imshow(H, vmin=0, vmax=10*H.mean(),\
				interpolation='nearest',
				origin='low',
				cmap=plt.get_cmap(cmap),
				extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    plt.show()

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
    """ Better fixed hexagonal structure with heavy bouncer """
    apos = read_pos('data/single_ball.dat')

    t           = [pos[0] for pos in apos]
    z_membrane  = [pos[1] for pos in apos]
    x_ball      = [pos[2] for pos in apos]
    y_ball      = [pos[3] for pos in apos]
    z_ball      = [pos[4] for pos in apos]

    plt.plot(t, z_ball, c='black')
    plt.plot(t, z_membrane, c='green')
    plt.legend(['ball', 'membrane'], loc = 'center right')
    plt.show()

    plt.plot(x_ball, y_ball)
    plt.show()

if __name__ == '__main__':
    """ %run this.file.py """
    show_single_ball()
