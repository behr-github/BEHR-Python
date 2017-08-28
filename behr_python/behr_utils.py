#!/usr/bin/env python3

import datetime as dt
import numpy as np
import os.path

from . import behr_constants as constants
from . import readwrite as rw

class InputError(Exception):
    pass

def validate_path(path_in, var_name):
    if not isinstance(path_in, str):
        raise InputError('{} must be a string'.format(var_name))
    elif not os.path.isdir(path_in):
        raise InputError('{} ({}) does not exist'.format(var_name, path_in))


def construct_behr_filename(file_date):
    if not isinstance(file_date, (dt.datetime, dt.date)):
        raise InputError('file_date must be an instance of datetime.date or datetime.datetime')

    return 'OMI_BEHR_{}_{}.hdf'.format(constants.behr_version, file_date.strftime('%Y%m%d'))

def construct_sp_filename(file_date):
    if not isinstance(file_date, (dt.datetime, dt.date)):
        raise InputError('file_date must be an instance of datetime.date or datetime.datetime')

    return 'OMI_SP_{}_{}.hdf'.format(constants.behr_version, file_date.strftime('%Y%m%d'))


def read_scattering_weights(sw_file):
    with open(sw_file, 'r') as f:
        pass


def read_temperature_profiles(prof_file):

    # This is a messy file format. There's not a lot of in-file indicators that we can scan for, so
    # we just have to "know" what each section is
    with open(prof_file, 'r') as f:
        # The first two lines are a header and a blank line
        for i in range(2):
            _ = f.readline()

        # The next lines define the number of pressure, the range of longitudes, the range of latitudes,
        # and the range of months, in that order
        npres = int(f.readline())
        lon_info = [float(x) for x in f.readline().split()]
        lon_info[0] = int(lon_info[0])
        lat_info = [float(x) for x in f.readline().split()]
        lat_info[0] = int(lat_info[0])
        month_info = [int(float(x)) for x in f.readline().split()]

        _ = f.readline() # blank line

        # The next three lines define the pressures that the temperatures are defined at
        pres = []
        for i in range(3):
            line = f.readline().split()
            for x in line:
                pres.append(float(x))
        if len(pres) != npres:
            raise IOError('Read the wrong number of pressures')
        else:
            pres = np.array(pres)

        # Go ahead and define the longitude, latitude, and month dimensions as well
        # Lat & lon are defined in the middle, but the start and stop values are at edges,
        # so add 0.5. Since arange()'s end is exclusion, but the stop value is the last edge
        # we don't need to adjust it.
        lon_step = (lon_info[2] - lon_info[1])/lon_info[0]
        lons = np.arange(lon_info[1]+0.5*lon_step, lon_info[2], lon_step)
        lat_step = (lat_info[2] - lat_info[1])/lat_info[0]
        lats = np.arange(lat_info[1]+0.5*lat_step, lat_info[2], lat_step)
        months = np.arange(month_info[1], month_info[2])

        # Allow the array to be in C order, where the most rapidly iterated dimension is last
        temperature = np.empty((months.size, lats.size, lons.size, pres.size), dtype=np.float64)

        file_iter = rw.scan_file(f)

        for i_month in range(months.size):
            for i_lat in range(lats.size):
                for i_lon in range(lons.size):
                    for i_pres in range(pres.size):
                        try:
                            temperature[i_month, i_lat, i_lon, i_pres] = float(next(file_iter))
                        except StopIteration:
                            raise IOError('Reached end of {} too soon'.format(f.name)) from None

    return temperature, pres, lons, lats, months


