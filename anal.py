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

    plt.plot(x)
    plt.plot(y)
    plt.plot(z)
    plt.legend(['x', 'y', 'z'])
    plt.show()
