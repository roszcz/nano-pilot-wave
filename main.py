from subprocess import call
from matplotlib import pyplot as plt
import os
import anal

if __name__ == '__main__':
    """ Run lammps multiple times with python main.py """

    gravities = [7.5 + 0.1 * it for it in range(20)]

    template_file   = 'in.pilot_template.lamps'
    final_file	    = 'in.RUNME.lamps'

    score_file	    = 'data/single_ball.dat'

    processess = '4'

    commands = ['mpirun', '-np', processess,
		'lammps-daily',
		'-sf', 'omp',
		'-pk', 'omp', processess,
		'-in', final_file]

    gravity_marker = '${GRAVITY}'

    # Prepare score containers
    balls_z = []
    membranes_z = []

    for gravity in gravities:
	with open(final_file, 'wt') as fout:
	    with open(template_file, 'rt') as fin:
		for line in fin:
		    fout.write(\
			 line.replace(gravity_marker, str(gravity)))

	print "Running with gravity:", gravity

	call(commands, stdout=open(os.devnull, 'wb'))

	score = anal.read_pos(score_file)

	balls_z.append([pos[4] for pos in score])
	membranes_z.append([pos[1] for pos in score])

    plt.imshow(balls_z)
    plt.show()
    plt.imshow(membranes_z)
    plt.show()
