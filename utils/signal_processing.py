import numpy as np
from typing import List, Optional, Literal, Tuple

import pandas as pd


# ==========================================
# ============ TIME SERIES FCN =============
# ==========================================
def ts_custom_split(df: pd.DataFrame,
                    svec: Optional[np.ndarray] = None,
                    test: float = 0.2,
                    how: Literal['ordered', 'shuffled'] = 'ordered',
                    random_seed: Optional[int] = 42) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:

    # This function performs train/test split on dataframes
    # in preparation for modelling/pipeline
    # Returns 2datatframes, the size of which is specified by the arguments TEST

    # Deterimine frame limits
    if df is None:
        return None, None, None
    # Make split
    n_smp = len(df)
    tstart = int( (1-test) * n_smp )
    if how=='ordered':
        # Splits are chronologically ordered
        # Make splits
        xtrain = df.iloc[:tstart]
        xtest = df.iloc[tstart:]
    elif how=='shuffled':
        if svec is None:
            svec = np.random.permutation(n_smp)
        # Slice X matrix
        xtrain = df.iloc[svec[:tstart]]
        xtest = df.iloc[svec[tstart:]]
        svec = svec[tstart:]
    else:
        raise NotImplementedError('This split type is not implemented yet')
    return xtrain, xtest, svec
