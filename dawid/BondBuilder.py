import numpy as np
import math
import argparse


def create_atoms(N, M, a, origin, function=None):
    """ Creates NxM hexagonialish grid with *a* grid constant """
    # Translation unit vector
    ay = -a * math.sqrt(3)/2.0
    ax = -a * 0.5

    # Container for atoms' xyz positions
    # TODO, why not (N, M, 3)
    atoms = np.empty((N * M, 3), dtype=float)
    for n in xrange(N):
        for m in xrange(M):
            x = ax*n + a*m
            y = ay*n
            id_ = n*M + m
            atoms[id_][0] = x + origin[0]
            atoms[id_][1] = y + origin[1]
            atoms[id_][2] = origin[2]

    # This allows to select which atoms should be active
    # TODO refactor out
    if function is None:
        active_atoms = np.ones((N, M), dtype=bool)
    else:
        active_atoms = np.zeros((N, M), dtype=bool)
        for n in xrange(N):
            for m in xrange(M):
                id_ = n*M + m
                if function(atoms[id_]):
                    active_atoms[n][m] = True

    return (atoms, active_atoms)

def get_bonds(N, M, avail_atoms=None):
    """ Create bonds """
    # % M ->
    # N\/

    if avail_atoms is None:
        active_atoms = np.ones((N, M), dtype=bool)
    else:
        active_atoms = np.copy(avail_atoms)

    # Nieghboring cells
    shifts = [[-1, -1], [-1, 0], [0, 1], [1, 1], [1, 0], [0, -1]]

    bonds_possible = N*M*6
    bonds_list = np.zeros((bonds_possible, 2), dtype=int)
    bonds_count = 0

    for n in xrange(N):
        for m in xrange(M):
            local_id = n*M+m
            if active_atoms[n][m] == False:
                continue
            active_atoms[n][m] = False

            for s in shifts:
                neigh_n = n+s[0]
                neigh_m = m+s[1]
                nlocal_id = neigh_n*M+neigh_m

                if neigh_m < 0 or neigh_m >= M or neigh_n < 0 or neigh_n >= N:
                    continue

                if active_atoms[neigh_n][neigh_m]:
                    bonds_list[bonds_count][0] = local_id
                    bonds_list[bonds_count][1] = nlocal_id

                    bonds_count += 1

    return (bonds_list, bonds_count)

def write_bonds_atoms(N, M, atoms, active_atoms, bonds_list,
                      bonds_count, name="o.xyz"):
    f = open("o.xyz", "w")
    atoms_count = np.count_nonzero(active_atoms)
    total = atoms_count + bonds_count
    f.write("%i\n%i" % (total, total))

    for n in xrange(N):
        for m in xrange(M):
            if active_atoms[n][m]:
                id_ = n*M + m
                a = atoms[id_]
                f.write("\nC %f %f %f" % (a[0], a[1], a[2]))

    for i in xrange(bonds_count):
        bond = bonds_list[i]
        at = 0.5*(atoms[bond[0]] + atoms[bond[1]])
        f.write("\nH %f %f %f" % (at[0], at[1], at[2]))

    f.close()


def write_membrane(N, M, atoms, active_atoms, bonds_list, bonds_count,
                   box_size, name="o.dat"):
    atoms_count = np.count_nonzero(active_atoms)

    # write header
    f = open(name, 'w')
    f.write("# Pilot wave dat file. \n\n")

    f.write(" %i atoms\n" % atoms_count)
    f.write(" %i bonds\n\n" % bonds_count)

    f.write(" 2 atom types\n")
    f.write(" 1 bond types\n\n")

    f.write(" %f %f xlo xhi\n" % (box_size[0][0], box_size[0][1]))
    f.write(" %f %f ylo yhi\n" % (box_size[1][0], box_size[1][1]))
    f.write(" %f %f zlo zhi\n\n" % (box_size[2][0], box_size[2][1]))

    f.write(" Atoms\n")
    id_proxy = {}
    id_final = 0
    for n in xrange(N):
        for m in xrange(M):
            if active_atoms[n][m]:
                id_final += 1
                id_ = n*M + m
                id_proxy[id_] = id_final
                a = atoms[id_]
                f.write("\n%i 0 1 %f %f %f" % (id_final, a[0], a[1], a[2]))

    f.write("\n\n Bonds\n")

    for i in xrange(bonds_count):
        bond = bonds_list[i]
        f.write("\n%i 1 %i %i" % (i+1, id_proxy[bond[0]], id_proxy[bond[1]]))


def write_membrane_force(N, M, atoms, active_atoms, bonds_list, bonds_count,
                         box_size, z_shift=10, name="o.dat"):
    atoms_count = np.count_nonzero(active_atoms)

    atoms_total = atoms_count*2
    bonds_total = bonds_count + atoms_count

    # write header
    f = open(name, 'w')
    f.write("# Pilot wave dat file. \n\n")

    f.write(" %i atoms\n" % atoms_total)
    f.write(" %i bonds\n\n" % bonds_total)

    f.write(" 3 atom types\n")
    f.write(" 2 bond types\n\n")

    f.write(" %f %f xlo xhi\n" % (box_size[0][0], box_size[0][1]))
    f.write(" %f %f ylo yhi\n" % (box_size[1][0], box_size[1][1]))
    f.write(" %f %f zlo zhi\n\n" % (box_size[2][0], box_size[2][1]))

    f.write(" Atoms\n")
    id_proxy = {}
    id_final = 0
    for n in xrange(N):
        for m in xrange(M):
            if active_atoms[n][m]:
                id_final += 1
                id_ = n*M + m
                id_proxy[id_] = id_final
                a = atoms[id_]
                f.write("\n%i 0 1 %f %f %f" % (id_final, a[0], a[1], a[2]))

    for n in xrange(N):
        for m in xrange(M):
            if active_atoms[n][m]:
                id_final += 1
                id_ = n*M + m
                a = atoms[id_]
                f.write("\n%i 0 3 %f %f %f" % (id_final, a[0], a[1], a[2] - z_shift))



    f.write("\n\n Bonds\n")

    for i in xrange(bonds_count):
        bond = bonds_list[i]
        f.write("\n%i 1 %i %i" % (i+1, id_proxy[bond[0]], id_proxy[bond[1]]))

    for i in xrange(atoms_count):
        f.write("\n%i 2 %i %i" % (i+1+bonds_count, i+1, i+1+atoms_count))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=["simple", "forcelayer"],
                        default="forcelayer",
                        help="type of generated system")
    parser.add_argument('-o', '--output', default='o.dat',
                        help="output data file name")
    parser.add_argument('-x', '--xyz', default=None,
                        help="output preview")
    parser.add_argument('-r', '--radius', type=float, default=100,
                        help="membrane radius")
    parser.add_argument('-a', '--spacing', type=float, default=1.0,
                        help="nodes spacing")
    parser.add_argument('-d', '--displace', type=float, default=20.0,
                        help="distance between force layer and membrane")
    parser.add_argument('-z', '--zdim', type=float, default=50.0,
                        help="z dim box size")

    args = parser.parse_args()

    r = args.radius
    a = args.spacing
    z_dim = args.zdim

    print "radius = ", r
    print "spacing = ", a
    print "layers spacing = ", args.displace
    print "sys type = ", args.type
    print "xyz preview = ", args.xyz
    print "output file = ", args.output

    offset = 5*a
    ay = a*math.sqrt(3)*0.5
    H = float((r+offset)*2)
    N = int(math.ceil(H/ay))
    M = N

    xo = -(math.sqrt(3)/3)*(H/2.0)
    yo = H/2.0

    origin = np.array([xo, yo, 0.0], dtype=float)

    r2 = r*r
    fun = lambda x: x[0]*x[0] + x[1]*x[1] < r2

    atoms, active_atoms = create_atoms(N, M, a, origin, function=fun)
    bonds_list, bonds_count = get_bonds(N, M, avail_atoms=active_atoms)

    if args.xyz:
        write_bonds_atoms(N, M, atoms, active_atoms, bonds_list, bonds_count,
                          name=args.xyz)

    box_size = [[-r-offset, r+offset], [-r-offset, r+offset], [-z_dim, z_dim]]
    if args.type == 'forcelayer':
        write_membrane_force(N, M, atoms, active_atoms, bonds_list,
                             bonds_count, box_size,
                             z_shift=args.displace, name=args.output)
    elif args.type == 'simple':
        write_membrane(N, M, atoms, active_atoms, bonds_list, bonds_count,
                       box_size, name=args.output)


if __name__ == "__main__" :
    main()
