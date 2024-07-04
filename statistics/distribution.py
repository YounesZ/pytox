import numpy as np
from typing import Tuple, Union, List
from submodules.pytox.utils.decorators import validate_arguments


@validate_arguments
def find_cumulative_threshold(x: np.ndarray,
                              y: np.ndarray,
                              thresh: float) -> Tuple[int, float, float]:
    """
    This function finds the value in a x,y function that corresponds
    to a certain threshold of its cumulative distribution
    """
    # Make sure it's a distribution
    y_ = y / np.sum(y)

    # Compute cumulative distribution
    y_c = np.cumsum(y_)

    # Compute average price
    avg = np.sum(y_ * x)

    # Check if interpolation is needed
    if thresh in y_c:
        ix__ = np.where(y_c==thresh)[0][0]
        return int(ix__), float(x[ix__]), avg
    else: # interpolate
        lower = np.sum(thresh > y_c) - 1
        if lower == -1:
            ix = int(1)
            ii = float(x[1])
        else:
            # X index
            ix = (thresh-y_c[lower]) * (lower+1) + (y_c[lower+1]-thresh) * lower
            ix = int( ix / (y_c[lower + 1] - y_c[lower]) )
            # X value
            ii = (thresh - y_c[lower]) * x[lower + 1] + (y_c[lower + 1] - thresh) * x[lower]
            ii = float(ii / (y_c[lower + 1] - y_c[lower]))
        return ix, ii, avg


@validate_arguments
def find_proba_for_value(x: Union[List, np.ndarray],
                         y: Union[List, np.ndarray],
                         value: float) -> float:

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
        return 2.0
    elif value in x:
        return y_c[np.where(x==value)[0][0]]
    elif value > x[-1]:     # Hyper expensive
        return 1.0
    elif value < x[0]:      # Hyper cheap
        return 0.0

    else: # interpolate
        lower = np.sum(value > x) - 1
        xspan = x[lower+1] - x[lower]
        # X index
        p = (value-x[lower]) * y_c[lower+1] + (x[lower+1]-value) * y_c[lower]
        p = p / xspan
        return p
