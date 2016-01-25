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

if __name__ == '__main__':
    
    apos = read_pos('data/a_fullerene_pos.dat')
