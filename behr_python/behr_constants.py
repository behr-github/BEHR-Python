import numpy as np
import os.path

_mydir = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))

behr_version = '2-1C'
behr_pres_levels = np.array([1020, 1015, 1010, 1005, 1000, 990, 980, 970, 960, 945, 925, 900, 875, 850,
                             825, 800, 770, 740, 700, 660, 610, 560, 500, 450, 400, 350, 280, 200])
temperature_prof_file = os.path.join(_mydir, 'resources', 'nmcTmpYr.txt')
scattering_wt_file = os.path.join(_mydir, 'resources', 'damf.txt')