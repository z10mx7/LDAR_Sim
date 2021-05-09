"""[summary]
    """
import scipy
import numpy as np
from leak_processing.unit_converter import gas_convert


def fit_dist(samples=None, fit_params=None, dist_type="lognorm", floc=0,  mu=None, sigma=None):
    dist = getattr(scipy.stats, dist_type)
    if samples is not None:
        # Lognormal cannot have 0 values
        if dist_type == "lognorm":
            samples = [s for s in samples if s > 0]
        param = dist.fit(samples, floc=floc)
        loc = param[-2],
        scale = param[-1]
        shape = param[:-2]
    elif fit_params is not None:
        loc = fit_params[-2],
        scale = fit_params[-1]
        shape = fit_params[:-2]
    elif mu and dist_type == "lognorm":
        loc = 0
        scale = np.exp(mu)
        shape = [sigma]
    return dist(*shape, loc=loc, scale=scale)


def leak_rvs(distribution, max_size=None, gpsec_conversion=None):
    """ Generate A random Leak, convert to g/s then checkit against
        leaks size, run until leak is smaller than max size

    Args:
        distribution (A scipy Distribution): Distribution of leak sizes
        max_size (int, optional): Maximum Leak Size
        gpsec_conversion (array, optional):  Conversion Units [input_metric, input_increment]

    Returns:
        [type]: [description]
    """

    while True:
        leaksize = distribution.rvs()  # Get Random Value from Distribution
        if gpsec_conversion and  \
                gpsec_conversion[0].lower() != 'gram' and \
                gpsec_conversion[1].lower() != "second":
            leaksize = gas_convert(leaksize, input_metric=gpsec_conversion[0],
                                   input_increment=gpsec_conversion[1])
        if not max_size or leaksize < max_size:
            break  # Rerun if value is larger than maximum
    return leaksize