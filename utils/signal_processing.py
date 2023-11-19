import numpy as np


# ==========================================
# ============ TIME SERIES FCN =============
# ==========================================
def ts_custom_split(df, svec=None, test=0.2, how='ordered', random_seed=42):
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


def get_sample_variables(df):
    if ('firstSampleTime' in df) and ('lastSampleTime' in df):
        sample_vars = ['firstSampleTime', 'lastSampleTime']
    elif ('slipStartSampleTime' in df) and ('slipStopSampleTime' in df):
        sample_vars = ['slipStartSampleTime', 'slipStopSampleTime']
    else:
        raise ValueError("Could not find start/stop variables in dataframe")
    return sample_vars
