#!/usr/bin/env python3

import datetime as dt
import os.path

from . import behr_utils as utils
from . import behr_constants as constants
from . import readwrite as rw
from . import behr_core as core

def behr_main(start_date=dt.date(2005, 1, 1), end_date=dt.date.today(), behr_mat_dir=None, sp_mat_dir=None, no2_profile_path=None,
              overwrite=False, profile_mode='monthly', DEBUG_LEVEL=2):

    # Input validation
    if not isinstance(start_date, (dt.date, dt.datetime)):
        raise utils.InputError('start_date must be a datetime.date or datetime.datetime instance')
    if not isinstance(end_date, (dt.date, dt.datetime)):
        raise utils.InputError('start_date must be a datetime.date or datetime.datetime instance')

    if behr_mat_dir is not None:
        utils.validate_path(behr_mat_dir, 'behr_mat_dir')
    if sp_mat_dir is not None:
        utils.validate_path(sp_mat_dir, 'sp_mat_dir')
    if no2_profile_path is not None:
        utils.validate_path(no2_profile_path, 'no2_profile_path')

    if not isinstance(overwrite, bool):
        raise utils.InputError('overwrite must be a bool')

    allowed_prof_modes = ('monthly', 'daily')
    if not isinstance(profile_mode, 'str') or profile_mode.lower() not in allowed_prof_modes:
        raise utils.InputError('profile_mode must be one of the strings {}'.format(', '.join(allowed_prof_modes)))

    if not isinstance(DEBUG_LEVEL, int) or DEBUG_LEVEL < 0:
        raise utils.InputError('DEBUG_LEVEL must be a positive integer')

    # ********* #
    # MAIN LOOP #
    # ********* #

    curr_date = start_date
    while curr_date <= end_date:
        if DEBUG_LEVEL > 0:
            print('Now processing {}'.format(curr_date))

        behr_file = os.path.join(behr_mat_dir, utils.construct_behr_filename(curr_date))
        if os.path.isfile(behr_file) and not overwrite:
            if DEBUG_LEVEL > 0:
                print('  File already exists, skipping')
                continue

        sp_file = os.path.join(sp_mat_dir, utils.construct_sp_filename(curr_date))
        if not os.path.isfile(sp_file):
            raise IOError('SP file {} not found'.format(sp_file))

        Data = rw.read_behr_hdf(sp_file)
        for swath in Data:
            core.behr_driver(swath, curr_date.year, curr_date.month, curr_date.day)