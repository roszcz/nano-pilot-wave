"""
This module is used to analyze simulation results.



"""
import numpy
import math
# TO DO: set proper logger! !!
import logging as log
log.basicConfig(format="%(levelname)s: %(message)s", level=10)


class traj:
    def __init__(self, filename, format='lammpstrj', log_level=10):
        """
        Args:
            filename: filename for reading
            format: format of the readed file
        """

        try:
            self.infile = open(filename, 'r')
            log.info("Successfully opened file: %s" % filename)
        except IOError:
            log.error("Could not find/read file: %s" % filename)

        function_name = "_read_" + format
        try:
            self.call_read = getattr(self, function_name)
        except AttributeError:
            log.error("Unknow file format: %s" % str(format))

    def read(self, read_n=-1):
        """
        Reads trajectory file frame by frame

        Args:
            read_n: number of trajestories to read
            read_n = -1: read the whole file
        Returns:
            list of frames
        """

        read_whole = False if read_n > 0 else True
        frame = True

        frames = []
        log.info("Read %i frames" % read_n)
        frames_readed = 0
        read_begining = str(read_n) if read_n > 0 else "INF"
        while frame and (read_n or read_whole):
            frame = self.call_read(False)
            if frame:
                frames_readed += 1
                frames.append(frame)
                log.info("Current frame (%i / %s)" %
                         (frames_readed, read_begining))

            read_n -= 1

        return frames

    def skip(self, skip_n=1):

        not_end = 1
        skip_begining = skip_n
        log.info("Skip %i frames" % skip_n)
        while not_end and skip_n:
            not_end = self.call_read(True)
            skip_n -= 1

        if not not_end:
            skipped = skip_begining - skip_n
            log.warning("After %i frames skipped end of file encountered" %
                        skipped)

    def _read_lammpstrj(self, skip):
        infile = self.infile
        frame_info = {}

        line = infile.readline()
        if not line:
            return False

        # loop over all header lines
        key_field_name = line.split()[1]
        while key_field_name != "ATOMS":
            if key_field_name == "TIMESTEP":
                timestep = int(infile.readline().split()[0])
                frame_info['timestep'] = int(timestep)

            elif key_field_name == "NUMBER":
                frame_atoms = int(infile.readline().split()[0])
                frame_info['atoms'] = int(frame_atoms)

            elif key_field_name == "BOX":
                box_size = []
                sl = infile.readline().split()
                box_size.append([float(sl[0]), float(sl[1])])
                sl = infile.readline().split()
                box_size.append([float(sl[0]), float(sl[1])])
                sl = infile.readline().split()
                box_size.append([float(sl[0]), float(sl[1])])

                frame_info['box'] = box_size

            elif key_field_name == "TIME":
                time_real = float(infile.readline().split()[0])
                frame_info['time'] = time_real

            else:
                log.warn("Unknow key field name: %s" % key_field_name)

            line = infile.readline()
            key_field_name = line.split()[1]

        # Prepare memory strusture on the header basis
        sp = line.split()
        key_fields = sp[2:]

        # key field groups (coords and velocity)
        # flags value meaning
        #   False - not set
        #   1 - set but memory unallocated
        #   2 - set and memory is allocated
        if 'x' in key_fields and 'y' in key_fields and 'z' in key_fields:
            coords_group = 1
        else:
            coords_group = False

        if 'xs' in key_fields and 'ys' in key_fields and 'zs' in key_fields:
            coords_s_group = 1
        else:
            coords_s_group = False

        if 'xu' in key_fields and 'yu' in key_fields and 'zu' in key_fields:
            coords_u_group = 1
        else:
            coords_u_group = False

        if 'vx' in key_fields and 'vy' in key_fields and 'vz' in key_fields:
            velocity_group = 1
        else:
            velocity_group = False

        frame_info['format'] = []

        # transform key position index in file to index in output list
        key_proxy = [None]*len(key_fields)

        fields = []
        key_index = 0
        proxy_index = 0
        # id_field = -1
        coord_index = len(key_fields)
        velocity_index = len(key_fields)

        for key in key_fields:
            if coords_group and key in ['x', 'y', 'z']:
                if coords_group == 1:
                    coords_group = 2
                    coord_index = key_index
                    fields.append(numpy.zeros([frame_atoms, 3], dtype=float))
                    frame_info['format'].append('coords')
                    key_index += 1

                if key == 'x':
                    key_proxy[proxy_index] = [coord_index, 0]
                elif key == 'y':
                    key_proxy[proxy_index] = [coord_index, 1]
                elif key == 'z':
                    key_proxy[proxy_index] = [coord_index, 2]
                else:
                    log.error("Something strange happend"
                              " while assigning coordinates to field")

            elif coords_s_group and key in ['xs', 'ys', 'zs']:
                if coords_s_group == 1:
                    coords_s_group = 2
                    coord_index = key_index
                    fields.append(numpy.zeros([frame_atoms, 3], dtype=float))
                    frame_info['format'].append('coords_scaled')
                    key_index += 1

                if key == 'xs':
                    key_proxy[proxy_index] = [coord_index, 0]
                elif key == 'ys':
                    key_proxy[proxy_index] = [coord_index, 1]
                elif key == 'zs':
                    key_proxy[proxy_index] = [coord_index, 2]
                else:
                    log.error("Something strange happend"
                              " while assigning scaled coordinates to field")

            elif coords_u_group and key in ['xs', 'ys', 'zs']:
                if coords_u_group == 1:
                    coords_u_group = 2
                    coord_index = key_index
                    fields.append(numpy.zeros([frame_atoms, 3], dtype=float))
                    frame_info['format'].append('coords_unwrapped')
                    key_index += 1

                if key == 'xu':
                    key_proxy[proxy_index] = [coord_index, 0]
                elif key == 'yu':
                    key_proxy[proxy_index] = [coord_index, 1]
                elif key == 'zu':
                    key_proxy[proxy_index] = [coord_index, 2]
                else:
                    log.error("Something strange happend"
                              " while assigning unwrapped coordinates to field")

            elif velocity_group and key in ['vx', 'vy', 'vz']:
                if velocity_group == 1:
                    velocity_group = 2
                    velocity_index = key_index
                    fields.append(numpy.zeros([frame_atoms, 3], dtype=float))
                    frame_info['format'].append('velocity')
                    key_index += 1

                if key == 'vx':
                    key_proxy[proxy_index] = [velocity_index, 0]
                elif key == 'vy':
                    key_proxy[proxy_index] = [velocity_index, 1]
                elif key == 'vz':
                    key_proxy[proxy_index] = [velocity_index, 2]
                else:
                    log.error("Something strange happend"
                              " while assigning fields")

            elif key == 'type':
                fields.append(numpy.zeros(frame_atoms, dtype=int))
                frame_info['format'].append(key)
                key_proxy[proxy_index] = key_index
                key_index += 1

            elif key == 'id':
                # id_field = key_index
                fields.append(numpy.zeros(frame_atoms, dtype=int))
                frame_info['format'].append(key)
                key_proxy[proxy_index] = key_index
                key_index += 1

            elif key == 'element':
                frame_info['format'].append(key)
                # *TO DO* upgrade from simple python string list
                fields.append([None]*frame_atoms)
                key_proxy[proxy_index] = key_index
                key_index += 1
            else:
                fields.append(numpy.zeros(frame_atoms, dtype=float))
                frame_info['format'].append(key)
                key_proxy[proxy_index] = key_index
                key_index += 1
            proxy_index += 1

        if skip:
            for i in xrange(frame_atoms):
                infile.readline()
            return 1

        fields_n = proxy_index
        for i in xrange(frame_atoms):
            sp = infile.readline().split()

            for j in xrange(fields_n):
                jproxy = key_proxy[j]

                if isinstance(jproxy, list):
                    fields[jproxy[0]][i][jproxy[1]] = sp[j]
                elif jproxy is not None:
                    fields[jproxy][i] = sp[j]

        frame_output = [frame_info]
        frame_output.extend(fields)
        return frame_output

    def _read_xyz(self, skip):

        infile = self.infile
        frame_info = {}
        line = infile.readline()
        if not line:
            return False

        frame_atoms = int(line)
        frame_info['atoms'] = int(frame_atoms)

        line = infile.readline()
        frame_info['comment'] = line
        # * TO DO * allow the acceptance of dditional fields
        frame_info['fields'] = ['element', 'coords']

        coords = numpy.empty([frame_atoms, 3], dtype=float)
        elements = [None]*frame_atoms

        if skip:
            for i in xrange(frame_atoms):
                infile.readline()
            return 1

        for i in xrange(frame_atoms):
            sl = infile.readline().split()
            elements[i] = sl[0]
            coords[i][0] = sl[1]
            coords[i][1] = sl[2]
            coords[i][2] = sl[3]
        return [frame_info, elements, coords]


class rms:
    """
    Tool for calculating roughness of atomic scale surfaces

    Args:
        coords (numpy float list (n, 3)):
        r_sample : vdw radius of sample atoms
        r_probe : vdw radius of probe atom
        active_box (optional array (3,2)): box in which the atoms are included
        in rms calcuation, if None - program will find optimal box
    """
    def __init__(self, coords, r_sample, r_probe, active_box=None):
        self.coords = coords         # array of surface atoms coordinates
        self.r_sample = r_sample     # r vdw of surface atoms
        self.r_probe = r_probe       # r vdw of probe atom
        self.r = r_sample + r_probe  # total bond r vdw surface-probe
        self.r2 = self.r*self.r

        # set or find box in which surface atoms will be searched
        if active_box:
            self.set_active_box(active_box)
        else:
            self.set_active_box(self.find_activ_box())


    def set_active_box(self, active_box):
        try:
            self.active_box = numpy.array([[active_box[0][0], active_box[0][1]],
                                           [active_box[1][0], active_box[1][1]],
                                           [active_box[2][0], active_box[2][1]]],
                                          dtype=float)
        except:
            log.error("Wrong active_box variable format, should be:"
                      " [[xmin, xmax], [ymin, ymax], [zmin, zmax]]")

        if (active_box[0][0] >= active_box[0][1]):
            log.error("Ill-defined X demension for box")
        if (active_box[1][0] >= active_box[1][1]):
            log.error("Ill-defined Y demension for box")
        if (active_box[2][0] >= active_box[2][1]):
            log.error("Ill-defined Z demension for box")

    def find_activ_box(self, h_ratio=0.5):
        """
        Find box large enough to fit all atoms inside

        Args:
            h_ratio : what part of the atoms in the box will be used for
            claculations (atoms with higher z component will be accepted)
        """

        coords = self.coords
        xmax, ymax, zmax = coords.max(axis=0)
        xmin, ymin, zmin = coords.min(axis=0)

        return [[xmin, xmax], [ymin, ymax], [zmin, zmax]]

    def get_surf_array_oa2d(self, sampling_array, lc_rep=1):
        """

        Args:
            sampling_array : array of point for which height will be calculated
            lc_rep : how many logic cells will be taken to calculate one point
            1 - (square 3x3) 2 - (square 5x5) 3 - (square 7x7)  ...
        """

        # Step 1 - create array of logica cells
        # ------------------------------------
        r = self.r/float(lc_rep)
        lc_rep = int(lc_rep)
        active_box = self.active_box
        offset = 0.01

        x_dimension = active_box[0][1] - active_box[0][0] + offset
        y_dimension = active_box[1][1] - active_box[1][0] + offset

        x_rep = int(math.ceil(x_dimension/r))
        y_rep = int(math.ceil(y_dimension/r))

        logical_cells = numpy.zeros((x_rep, y_rep, 3), dtype=float)
        logical_cells.fill(active_box[2][0])

        x_shift = -active_box[0][0]
        y_shift = -active_box[1][0]

        coords = self.coords
        # loop over all atoms and assign them to the appropriate cells
        for i in xrange(len(coords)):
            x_index = int(math.floor(coords[i][0]+x_shift)/r)
            y_index = int(math.floor(coords[i][1]+y_shift)/r)
            z = coords[i][2]

            # only one atom with highest z per logic cell
            if z > logical_cells[x_index][y_index][2]:
                logical_cells[x_index][y_index][0] = coords[i][0]
                logical_cells[x_index][y_index][1] = coords[i][1]
                logical_cells[x_index][y_index][2] = z

        # Step 2 - using generated logical cells and points to sample
        # create array with corresponding heights
        # ------------------------------------

        x_index_max = int(x_rep - lc_rep)
        y_index_max = int(y_rep - lc_rep)

        #
        neigh_template = numpy.arange(-lc_rep, lc_rep+1, 1, dtype=int)

        surface_array = numpy.zeros((len(sampling_array), 3), dtype=float)
        for i in xrange(len(sampling_array)):
            # calculate index  corresponding to probe x y
            probe_xy = sampling_array[i]
            x_index = int(math.floor(probe_xy[0]+x_shift)/r)
            y_index = int(math.floor(probe_xy[1]+y_shift)/r)

            # check boundary conditions
            if x_index < lc_rep:
                x_neigh = neigh_template[(lc_rep-x_index):]+x_index
            elif x_index >= x_index_max:
                x_neigh = neigh_template[:(lc_rep+x_rep-x_index)]+x_index
            else:
                x_neigh = neigh_template+x_index

            if y_index < lc_rep:
                y_neigh = neigh_template[(lc_rep-y_index):]+y_index
            elif y_index >= y_index_max:
                y_neigh = neigh_template[:(lc_rep+y_rep-y_index)]+y_index
            else:
                y_neigh = neigh_template+y_index

            z = None
            # loop over all neighbors
            for x_n_index in x_neigh:
                for y_n_index in y_neigh:
                    z_new = self.calc_z_oa2d(probe_xy,
                                         logical_cells[x_n_index][y_n_index])
                    if z_new > z:
                        z = z_new

            surface_array[i][0] = probe_xy[0]
            surface_array[i][1] = probe_xy[1]
            surface_array[i][2] = z

        return surface_array

    def calc_z_oa2d(self, probe_xy, sample_atom):
        """

        """
        r2 = self.r2
        dx = probe_xy[0] - sample_atom[0]
        dy = probe_xy[1] - sample_atom[1]
        dxy2 = dx*dx + dy*dy
        z = sample_atom[2]

        if dxy2 > r2:
            return None
        else:
            return math.sqrt(r2-dxy2)+z
