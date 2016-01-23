import matplotlib.pyplot as plt
import numpy as np

def read_pos(filepath):
    out = []
    with open(filepath) as fin:
        for line in fin:
            vals = line.split()
            if len(vals) is 4:
                out.append([float(val) for val in vals])
    return out

if __name__ == "__main__":

    fpath = 'zball.dat'
    pos = read_pos(fpath)
    x = []
    y = []
    z = []
    for val in pos:
        x.append(val[1] - 80)
        y.append(val[2] - 80)
        z.append(val[3])

    plt.plot(x[1::2])
    plt.plot(y[1::2])
    plt.plot(z[1::2])
    plt.plot(x[0::2])
    plt.plot(z[0::2])
    plt.legend(['x2', 'y2', 'z2','x1', 'z1'])
    plt.show()
