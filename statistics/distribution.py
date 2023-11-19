import numpy as np


def find_cumulative_threshold(x, y, thresh):
    """
    This function finds the value in a x,y function that corresponds
    to a certain threshold of its cumulative distribution
    """
    # Make sure it's a distribution
    y_ = y / np.sum(y)

    # Compute cumulative distribution
    y_c = np.cumsum(y_)

    # Check if interpolation is needed
    if thresh in y_c:
        ix__ = np.where(y_c==thresh)[0][0]
        return ix__, x[ix__]
    else: # interpolate
        lower = np.sum(thresh > y_c) - 1
        # X index
        ix = (thresh-y_c[lower]) * (lower+1) + (y_c[lower+1]-thresh) * lower
        ix = ix / (y_c[lower + 1] - y_c[lower])
        # X value
        ii = (thresh - y_c[lower]) * x[lower + 1] + (y_c[lower + 1] - thresh) * x[lower]
        ii = ii / (y_c[lower + 1] - y_c[lower])
        return ix, ii


def find_proba_for_value(x, y, value):
    """
    This function finds the value in a x,y function that corresponds
    to a certain threshold of its cumulative distribution
    """
    # Make sure prices are an array
    if isinstance(x, list):
        x = np.array(x)

    # Make sure it's a distribution
    y_ = y / np.sum(y)

    # Compute cumulative distribution
    y_c = np.cumsum(y_)

    # Check if interpolation is needed
    if len(x)==0:
        return 2
    elif value in x:
        return np.where(x==value)[0][0]
    elif value > x[-1]:     # Hyper expensive
        return 1.
    elif value < x[0]:      # Hyper cheap
        return 0.

    else: # interpolate
        lower = np.sum(value > x) - 1
        # X index
        p = (value-x[lower]) * y_c[lower+1] + (x[lower+1]-value) * y_c[lower]
        return p
