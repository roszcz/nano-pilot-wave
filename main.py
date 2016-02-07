from subprocess import call
from matplotlib import pyplot as plt
import os
import anal
import pickle

template_file   = 'in.pilot_template.lamps'
final_file      = 'in.RUNME.lamps'

class LampsRunner(object):
    """ Convenience class for running lammps fro python """
    def __init__(self):
	""" Co robi traktor u fryzjera? Warkocze """
	self.gravity = '8.5'
	self.membrane_frequency = '1100'

    def set_gravity(self, grav):
	""" set me """
	self.gravity = str(grav)

    def set_membrane_frequency(self, freq):
	""" set me """
	self.membrane_frequency = str(freq)

    def make_file(self):
	""" Adjust this with the template file and changable parameters """
	# Prepare markers 
	gravity_marker	    = '${GRAVITY}'
	frequency_marker    = '${MEMBRANE_FREQUENCY}'

	# Mystic file operations
	with open(final_file, 'wt') as fout:
            with open(template_file, 'rt') as fin:
		for line in fin:
                    # Set gravity
                    newline = line.replace(gravity_marker,\
                                           self.gravity)
                    # Set frequency
                    newline = newline.replace(frequency_marker,\
                                              self.membrane_frequency)
                    fout.write(newline)

    def run_it(self):
	""" Runs lammps """
	self.make_file()
	processess = str(8)

	commands = ['mpirun', '-np', processess,
                    'lammps-daily',
                    '-sf', 'omp',
                    '-pk', 'omp', processess,
                    '-in', final_file]

	call(commands, stdout=open(os.devnull, 'wb'))

if __name__ == '__main__':
    """ Run lammps multiple times with python main.py """

    runner = LampsRunner()

    gravities   = [7 + 0.1 * it for it in range(7)]
    frequencies = [1010 + 5 * it for it in range(7)]

    score_file  = 'data/single_ball.dat'

    # Prepare score containers
    balls_z     = []
    membranes_z = []

    for gravity in gravities:
	for freq in frequencies:
            runner.set_membrane_frequency(freq)
            runner.set_gravity(gravity)

            print "Gravity:", gravity
            print "Frequency:", freq

            runner.run_it()

            score = anal.read_pos(score_file)

            balls_z.append([pos[4] for pos in score])
            membranes_z.append([pos[1] for pos in score])

            # Re-Save every step
            with open('data/ballsz.pickle', 'wb') as handle:
                pickle.dump(balls_z, handle)

            with open('data/membranesz.pickle', 'wb') as handle:
                pickle.dump(membranes_z, handle)

    # plt.imshow(balls_z, aspect='auto')
    # plt.show()
    # plt.imshow(membranes_z, aspect='auto')
    # plt.show()

