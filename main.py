from subprocess import call
from matplotlib import pyplot as plt
import os
import anal
import pickle

template_file   = 'in.pilot_template.lamps'
oscillator_file = 'in.oscillators.lamps'
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
        self.a_ball_z_marker     = 'A_BALL_HEIGHT'
        self.a_ball_z            = '-6.2'
        self.spring_marker       = 'SPRING_CONSTANT'
        self.spring_factor       = '0.5'
        self.a_mass_marker       = 'A_BALL_MASS'
        self.a_mass              = '392.01'
        self.iterations_marker   = 'ITERATIONS'
        self.iterations          = '20000'
        self.sheet_radius_m      = 'SHEET_RADIUS'
        self.sheet_radius        = '88'

        self.processes           = '8'

    def set_number_of_cores(self, howmany):
        """ how """
        self.processes = str(howmany)

    def set_sheet_radius(self, nm):
        """ this is necessary """
        self.sheet_radius = str(nm)

    def set_number_of_iterations(self, howmany):
        """ how long """
        self.iterations = str(howmany)

    def set_spring_constant(self, k):
        """ wtf units """
        self.spring_factor = str(k)

    def set_a_ball_height(self, angstroms):
        """ how high """
        self.a_ball_z = str(angstroms)

    def set_amplitude(self, amp):
        """ futro odrosnie jutro """
        self.amplitude = str(amp)

    def set_a_ball_mass(self, kg):
        """ time of flight should not be related to the mass """
        self.a_mass = str(kg)

    def set_gravity(self, grav):
	""" kontempluj przejaw tao """
	self.gravity = str(grav)

    def set_membrane_frequency(self, freq):
	""" set me """
	self.membrane_frequency = str(freq)

    def run_it(self, filepath):
	""" Runs lammps """
	commands = ['mpirun', '-np', self.processes,
                    'lammps-daily',
                    '-sf', 'omp',
                    '-pk', 'omp', self.processes,
                    '-var', self.amp_marker, self.amplitude,
                    '-var', self.gravity_marker, self.gravity,
                    '-var', self.spring_marker, self.spring_factor,
                    '-var', self.a_ball_z_marker, self.a_ball_z,
                    '-var', self.frequency_marker, self.membrane_frequency,
                    '-var', self.a_mass_marker, self.a_mass,
                    '-var', self.sheet_radius_m, self.sheet_radius,,
                    '-var', self.iterations_marker, self.iterations,
                    '-in', filepath]

        # FIXME wtf why is this faster
	commands2= ['lammps-daily',
                    '-var', self.amp_marker, self.amplitude,
                    '-var', self.gravity_marker, self.gravity,
                    '-var', self.spring_marker, self.spring_factor,
                    '-var', self.a_ball_z_marker, self.a_ball_z,
                    '-var', self.frequency_marker, self.membrane_frequency,
                    '-var', self.a_mass_marker, self.a_mass,
                    '-var', self.sheet_radius_m, self.sheet_radius,,
                    '-var', self.iterations_marker, self.iterations,
                    '-in', filepath]

	# call(commands2, stdout=open(os.devnull, 'wb'))
	call(commands2)

if __name__ == '__main__':
    """ Run lammps multiple times with python main.py """

    runner = LampsRunner()

    gravities       = [10]
    frequencies     = [1000]
    amplitudes      = [0.05]
    a_ball_zs       = [-9]
    # 102.01 and 112.01 gave great results
    a_ball_mass     = [102.51]
    spring_factors  = [1.12]
    sheet_radius    = 90


    score_file  = 'data/single_ball.dat'
    # score_file  = 'data/oscillations.dat'

    # Prepare score containers
    balls_z     = []
    membranes_z = []

    for gravity in gravities:
	for freq in frequencies:
            for amp in amplitudes:
                for height in a_ball_zs:
                    for kz in spring_factors:
                        for mass in a_ball_mass:
                            runner.set_a_ball_mass(mass)
                            runner.set_membrane_frequency(freq)
                            runner.set_gravity(gravity)
                            runner.set_amplitude(amp)
                            runner.set_a_ball_height(height)
                            runner.set_spring_constant(kz)

                            print "Gravity:", gravity
                            print "Frequency:", freq
                            print "Amplitude:", amp
                            print "Ball wysokosc:", height
                            print "Spring constant:", kz
                            print "Ball's mass:", mass

                            runner.set_sheet_radius(sheet_radius)
                            print "Radius of sheet:", sheet_radius

                            runner.set_number_of_iterations(50000000)
                            runner.set_number_of_cores(4)
                            runner.run_it(template_file)

                            score = anal.read_pos(score_file)

                            # For oscillations related reaserch we only have one position in that file
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

