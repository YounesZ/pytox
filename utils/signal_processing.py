import numpy as np
from typing import List, Optional, Literal, Tuple
from submodules.pytox.utils.decorators import validate_arguments


import pandas as pd


# ==========================================
# ============ TIME SERIES FCN =============
# ==========================================
@validate_arguments
def ts_custom_split(df: pd.DataFrame,
                    svec: np.ndarray,
                    test: float = 0.2,
                    how: Literal['ordered', 'shuffled'] = 'ordered',
                    random_seed: Optional[int] = 42) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:

    # This function performs train/test split on dataframes
    # in preparation for modelling/pipeline
    # Returns 2datatframes, the size of which is specified by the arguments TEST

    # Make split
    n_smp = len(df)
    tstart = int( (1-test) * n_smp )
    if how=='ordered':
        # Splits are chronologically ordered
        # Make splits
        xtrain = df.iloc[:tstart]
        xtest = df.iloc[tstart:]
    elif how=='shuffled':
        if len(svec) != len(df):
            svec = np.random.permutation(n_smp)
        # Slice X matrix
        xtrain = df.iloc[svec[:tstart]]
        xtest = df.iloc[svec[tstart:]]
        svec = svec[tstart:]
    else:
        raise NotImplementedError('This split type is not implemented yet')
    return xtrain, xtest, svec
