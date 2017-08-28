#!/usr/bin/env python3

import h5py
from numpy import ma
import re

def read_behr_hdf(hdf_file):
    """
    Read a BEHR .hdf (version 5) file
    :param hdf_file: the path to the HDF file
    :return: a list of dictionaries that contain the data fields
    """

    # Assume that the HDF file is organized as /Data/SwathNNNNN
    data = []
    with h5py.File(hdf_file, 'r') as fobj:
        for swath in fobj['Data'].values():
            swath_dict = dict()
            for name, dset in swath.items():
                val = ma.masked_array(dset.value, mask=dset.value == dset.fillvalue)
                swath_dict[name] = val
            data.append(swath_dict)

    return data

def scan_file(fobj, delim=None, bufsize=1024):
    # Credit to Andrew Clark at https://stackoverflow.com/questions/10183784/is-there-a-way-to-read-a-file-in-a-loop-in-python-using-a-separator-other-than-n
    # with some modifications of my own
    # TODO: fix to handle if the buffer ends in the middle of a value or if the value is longer than the buffer
    delim_re = re.compile('\s$') if delim is None else re.compile('{}$'.format(delim))

    prev = ''
    while True:
        s = fobj.read(bufsize)
        if not s:
            break
        else:
            s = prev + s

        if delim is None:
            split = s.split()
        else:
            split = s.split(delim)

        if delim_re.search(s) is not None:
            # If the last character in the string is the delimiter, then we can just yield each split item
            # and not worry about the last item being split across two buffers
            for val in split:
                yield val
            prev = ''
        else:
            # If the last character in the buffer is not a delimiter, then we don't want to yield it because
            # it will be incomplete. Instead we combine it with the beginning of the next buffer.
            if len(split) > 1:
                for val in split[:-1]:
                    yield val
            prev = split[-1]
