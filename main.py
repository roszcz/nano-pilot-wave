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
	self.gravity_marker	 = 'GRAVITY'
	self.gravity             = '8.5'
	self.frequency_marker    = 'MEMBRANE_FREQUENCY'
	self.membrane_frequency  = '1100'
        self.amp_marker          = 'AMPLITUDE'
        self.amplitude           = '0.33'

    def set_amplitude(self, amp):
        """ futro odrosnie jutro """
        self.amplitude = str(amp)

    def set_gravity(self, grav):
	""" kontempluj przejaw tao """
	self.gravity = str(grav)

    def set_membrane_frequency(self, freq):
	""" set me """
	self.membrane_frequency = str(freq)

    def run_it(self):
	""" Runs lammps """
	processess = str(8)

	commands = ['mpirun', '-np', processess,
                    'lammps-daily',
                    '-sf', 'omp',
                    '-pk', 'omp', processess,
                    '-var', self.amp_marker, self.amplitude,
                    '-var', self.gravity_marker, self.gravity,
                    '-var', self.frequency_marker, self.membrane_frequency,
                    '-in', template_file]

	call(commands, stdout=open(os.devnull, 'wb'))

if __name__ == '__main__':
    """ Run lammps multiple times with python main.py """

    runner = LampsRunner()

    gravities   = [8.2 + 0.1 * it for it in range(7)]
    frequencies = [1075]
    amplitudes  = [0.25 + 0.05 * it for it in range(20)]

    score_file  = 'data/single_ball.dat'

    # Prepare score containers
    balls_z     = []
    membranes_z = []

    for gravity in gravities:
	for freq in frequencies:
            for amp in amplitudes:
                runner.set_membrane_frequency(freq)
                runner.set_gravity(gravity)
                runner.set_amplitude(amp)

                print "Gravity:", gravity
                print "Frequency:", freq
                print "Amplitude:", amp

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

