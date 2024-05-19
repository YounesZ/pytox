import numpy as np


def compute_mean_abs_error(vec1: np.ndarray,
                           vec2: np.ndarray) -> float:

    err = -1
    if (len(vec1)>0) and (len(vec1)==len(vec2)):
        # Convert vectors to np arrays
        vec1 = np.array([float(i_) for i_ in vec1])
        vec2 = np.array([float(i_) for i_ in vec2])

        err = np.mean( np.abs(vec1 - vec2) )
    return err
