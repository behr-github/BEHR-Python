cimport numpy as np

from . import behr_constants

cpdef behr_driver(swath, int year, int month, int day):
    # Read in some variables to make the code less cumbersome
    cdef np.ndarray[np.float64_t, ndim=2] lon = swath['Longitude']
    cdef np.ndarray[np.float64_t, ndim=2] lat = swath['Latitude']
    cdef np.ndarray[np.float64_t, ndim=3] loncorns = swath['FoV75CornerLongitude']
    cdef np.ndarray[np.float64_t, ndim=3] latcorns = swath['FoV75CornerLatitude']
    cdef np.ndarray[np.float64_t, ndim=2] sza = swath['SolarZenithAngle']
    cdef np.ndarray[np.float64_t, ndim=2] vza = swath['ViewingZenithAngle']
    cdef np.ndarray[np.float64_t, ndim=2] raa = swath['RelativeAzimuthAngle']

    cdef np.ndarray[np.float64_t, ndim=1] pressure = behr_constants.behr_pres_levels

    cdef str temp_file = behr_constants.temperature_prof_file
    cdef str damf_file = behr_cosntants.scattering_wt_file