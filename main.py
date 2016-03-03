from subprocess import call
from matplotlib import pyplot as plt
import os
import anal as an
import pickle

template_file   = 'in.pilot_template.lamps'
oscillator_file = 'in.oscillators.lamps'

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
        self.mb_bond_marker      = 'MEM_K'
        self.mb_bond_k           = '0.6'
        self.mb_bond_r0_marker   = 'MEM_R0'
        self.mb_bond_r0          = '1.1'
        self.processes           = '8'

    def set_membrane_bond_harmonic_constant(self, kz):
        """ wow """
        self.mb_bond_k = str(kz)

    def set_mb_bond_r(self, angstroms):
        """ Equilibrium distance """
        self.mb_bond_r0 = str(angstroms)

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
        # Unix mp-ready version
	commands = ['mpirun', '-np', self.processes,
                    'lammps-daily',
                    '-var', self.amp_marker, self.amplitude,
                    '-var', self.gravity_marker, self.gravity,
                    '-var', self.spring_marker, self.spring_factor,
                    '-var', self.a_ball_z_marker, self.a_ball_z,
                    '-var', self.frequency_marker, self.membrane_frequency,
                    '-var', self.a_mass_marker, self.a_mass,
                    '-var', self.sheet_radius_m, self.sheet_radius,
                    '-var', self.iterations_marker, self.iterations,
                    '-var', self.mb_bond_marker, self.mb_bond_k,
                    '-var', self.mb_bond_r0_marker, self.mb_bond_r0,
                    '-in', filepath]

        # Windows slow version
	commands2= ['lmp_serial', '-i', filepath,
                    '-var', self.amp_marker, self.amplitude,
                    '-var', self.gravity_marker, self.gravity,
                    '-var', self.spring_marker, self.spring_factor,
                    '-var', self.a_ball_z_marker, self.a_ball_z,
                    '-var', self.frequency_marker, self.membrane_frequency,
                    '-var', self.a_mass_marker, self.a_mass,
                    '-var', self.sheet_radius_m, self.sheet_radius,
                    '-var', self.mb_bond_marker, self.mb_bond_k,
                    '-var', self.iterations_marker, self.iterations,
                    '-var', self.mb_bond_r0_marker, self.mb_bond_r0
                    ]

        # Silent
	# call(commands, stdout=open(os.devnull, 'wb'))

        # Verbose
	call(commands)

if __name__ == '__main__':
    """ Run lammps multiple times with python main.py """

    runner = LampsRunner()

    # Spring constant of the membrane points
    spring_factors  = 1.12
    runner.set_spring_constant(spring_factors)

    sheet_radius    = 90
    runner.set_sheet_radius(sheet_radius)

    # Membrane harmonic constant
    membrane_bond_ks = 0.6
    runner.set_membrane_bond_harmonic_constant(membrane_bond_ks)

    # Membrane bonds equilibric distances
    membrane_r_zeros = 1.76
    runner.set_mb_bond_r(membrane_r_zeros)

    # Freefall force
    gravity         = 13.01
    runner.set_gravity(gravity)

    # Membrane driving force frequency
    frequencies     = 1000
    runner.set_membrane_frequency(frequencies)

    # Drop the ball from
    a_ball_zs       = -7.6
    runner.set_a_ball_height(a_ball_zs)

    # Driving force amplitude
    amplitudes      = 0.05
    runner.set_amplitude(amplitudes)

    # 102.01 and 112.01 gave great results
    a_ball_mass     = [121 + 3 * it for it in range(1)]

    # Declare score paths
    ball_file = 'data/single_ball.dat'
    memb_file = 'data/membrane_pos.dat'

    # Prepare score containers
    balls_z     = []
    membranes_z = []

    # Final settings
    runner.set_number_of_iterations(int(12e7))
    runner.set_number_of_cores(8)

    for val in a_ball_mass:
        print 'current value is now set to: ', val
        # Set value to check and check
        runner.set_a_ball_mass(val)
        runner.run_it(template_file)
        # Read ball positions
        ball_score = an.read_pos(ball_file)
        bz = [pos[2] for pos in ball_score]
        balls_z.append(bz)

        # Membrane as well
        memb_score = an.read_pos(memb_file)
        mz = [pos[2] for pos in memb_score]
        membranes_z.append(mz)

        # Resave every iteration (you can see those live with ipython)
        with open('data/ball.pickle', 'wb') as fout:
            pickle.dump(balls_z, fout)
        with open('data/memb.pickle', 'wb') as fout:
            pickle.dump(membranes_z, fout)



    # score_file  = 'data/oscillations.dat'
    # anal.make_position_histogram(score_file)
