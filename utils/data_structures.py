import numpy as np
import pandas as pd
from os import path, listdir
from random import shuffle
from typing import List
from inspect import stack
from datetime import datetime
from itertools import compress



# ==========================================
# ============ DATA STRUCTURES =============
# ==========================================
def check_type(object, classcheck, path_to_code=''):
    if not isinstance(object, classcheck):
        # Find 2nd function in the stack
        stck = stack()
        stck_file = [i_ for i_ in stck if path_to_code in i_.filename]
        stck_file = stck_file[:2][-1].filename

        raise TypeError('The function %s was called with the wrong argument type:'
                        '\n\tinput argument type : %s'
                        '\n\texpected type: %s.' % (stck_file, type(object), classcheck.__name__)
                        )
    return


def replicate_until(obj, n, shuffle=False):
    # Check for type
    if isinstance(obj, list):
        obj = _replicate_list_until(obj, n, shuffle)
    elif isinstance(obj, pd.DataFrame):
        obj = _replicate_df_until(obj, n, shuffle)
    else:
        raise TypeError('Unknown type for object to replicate: %s' % type(obj))
    # Cut to right length
    obj = obj[:n]
    return obj


# ========================================
# ============ STRING CHAINS =============
# ========================================
def find_string_in_list(string, lst, is_string=True):
    bool = [string in i_ for i_ in lst]
    if is_string:
        elem = [i_ for i_ in lst if string in i_]
    else:
        elem = [i_ for i_ in lst if string not in i_]
    return bool, elem

def capitalize_first(string):
    assert isinstance(string, str)

    string_C = string
    if len(string)>0:
        string_C = string[0].upper() + string[1:].lower()
    return string_C

def remove_from_string(string, torem):
    # Make sure we can loop over strings to remove
    if not isinstance(torem, list):
        torem = list(torem)
    # Loop
    for i_ in torem:
        string_l = string.lower()
        i_l = i_.lower()
        if i_l in string_l:
            x_str, x_len = string_l.index(i_l), len(i_l)
            string = string[:x_str] + string[x_str+x_len:]
    return string


# ==========================================
# =========== STRUCTURE CHECKS =============
# ==========================================
def check_input(X, y=None, x_type=List[pd.DataFrame]):
    output = []
    for i_var in [X, y]:
        # Check input X
        if i_var is None:
            pass
        elif isinstance(i_var, list) and (x_type is list):
            pass
        elif isinstance(i_var, pd.DataFrame) and (x_type is List[pd.DataFrame]):
            i_var = [i_var]
        elif isinstance(i_var, pd.DataFrame) and (x_type is pd.DataFrame):
            pass
        elif isinstance(i_var, np.ndarray) and (x_type is np.ndarray):
            pass
        elif isinstance(i_var, np.ndarray) and (x_type is List[np.ndarray]):
            i_var = [i_var]
        elif not isinstance(i_var, list) and (x_type is list):
            i_var = [i_var]
        elif isinstance(i_var, list) and isinstance(i_var[0], np.ndarray) and (x_type is List[np.ndarray]):
            pass
        elif isinstance(i_var, list) and isinstance(i_var[0], pd.DataFrame) and (x_type is List[pd.DataFrame]):
            pass
        elif (x_type is List[np.ndarray]) and (not isinstance(i_var, list) or not isinstance(i_var[0], np.ndarray)):
            raise TypeError('The input X does not have the right format: should be %s'%x_type)
        elif (x_type is List[pd.DataFrame]) and (not isinstance(i_var, list) or not isinstance(i_var[0], pd.DataFrame)):
            raise TypeError('The input X does not have the right format: should be %s'%x_type)
        else:
            raise TypeError('Uncaught error - unrecognized input type')
        output += [i_var]

    # Check output
    if (not output[1] is None) and (len(output[0])!=len(output[1])):
        raise ValueError('X and y must have the same length')
    return output[0], output[1]


def convert_input(X, out_type=List[pd.DataFrame]):
    # Checks
    is_list = isinstance(X, list)
    if is_list:
        # Check elements type
        all_df = all(isinstance(i_, pd.DataFrame) for i_ in X)
        all_sr = all(isinstance(i_, pd.Series) for i_ in X)
        all_ar = all(isinstance(i_, np.ndarray) for i_ in X)
        if out_type is List[pd.DataFrame]:
            if all_sr:
                X = [i_.to_frame() for i_ in X]
            elif all_ar:
                X = [pd.DataFrame(data=i_) for i_ in X]
            elif all_df:
                pass
            else:
                raise TypeError('Could not convert list to List[pd.Dataframe]')
        elif out_type is List[np.ndarray]:
            if all_sr or all_df:
                X = [i_.astype(float).values for i_ in X]
            elif all_ar:
                pass
            else:
                raise TypeError('Could not convert list to List[pd.Dataframe]')
        else:
            raise TypeError('Can only convert a list to List[pd.DataFrame] or List[np.ndarray]')
    else:
        raise TypeError('Can only convert a lists')
    return X


# ======================================
# =========== DICTIONARIES =============
# ======================================
def serialize_dictionary(criteria):
    output = ''
    for i_ in criteria.keys():
        suffix = '-'.join([str(j_) for j_ in criteria[i_]])
        output += '%s--%s__' % (i_, suffix)
    output = output[:-2]
    return output


def flip_dict(dico):
    flipped = {}
    for k, v in dico.items():
        for i_ in v:
            flipped.update({i_: k})
    return flipped


# ======================================
# =========== PYTHON LISTS =============
# ======================================
def _replicate_list_until(ls, n, do_shuffle):
    # Compute number of replications
    n_rep = int(np.ceil(n / len(ls)))
    # Replicate structure
    lsrep = [ls] * n_rep
    # Concatenate structure
    lsrep = sum(lsrep, [])
    # Shuffle structure
    if do_shuffle:
        shuffle(lsrep)
    return lsrep


def is_list_of_strings(lst):
    # Determine elements types
    is_str = [isinstance(i_, str) for i_ in lst]
    if all(is_str):
        return True
    else:
        return False

def get_index_in_ordered_list(objval, vallist):
    # Check if object has a spot
    ix = None
    if objval < max(vallist):
        # Get insertion index
        nvalues = vallist + [objval]
        nvalues.sort()
        ix = nvalues.index(objval)
    return ix


def sorted_indices(lst):
    idx = [i[0] for i in sorted(enumerate(lst), key=lambda x: x[1])]
    idx = idx[::-1]
    return idx


# =======================================
# =========== PANDAS SERIES =============
# =======================================
def sample_as_distribution(srs, n_values, default_value=None):
    # Prep data structure
    n_total= srs.sum()

    if n_total>0:
        n_repl = np.ceil(n_values/n_total)
        srs = (srs * n_repl).astype(int)

        # Multiply with frequency
        replica = [[i] * j for i, j in zip(srs.index, srs.values)]
        replica = sum(replica, [])
        # Keep selected values
        shuffle(replica)
        distrib = replica[:n_values]
    else:
        distrib = [default_value] * n_values
    return distrib


def _replicate_df_until(df, n, shuffle):
    # Compute number of replications
    n_rep = int( np.ceil(n / len(df)) )

    # Reset index
    re_index = None
    if (len(df.index.names)>0) and (df.index.names[0] is not None):
        re_index = list(df.index.names)
        df = df.reset_index()

    # Replicate structure
    dfrep = pd.DataFrame(data=np.repeat(df.to_numpy(), n_rep, axis=0),
                         columns=df.columns)
    # Shuffle dataframe
    if shuffle:
        dfrep = dfrep.sample(frac=1)

    # Re-index
    if not re_index is None:
        dfrep = dfrep.set_index(re_index)

    return dfrep


# ======================= #
# ===---    I/O    ---=== #
# ======================= #
def append_csv(df, file_path):

    # If the file exists already, append data
    if path.isfile(file_path):
        # Load file
        df_all = pd.read_csv(file_path, index_col=0)
        # Concatenate dataframes
        df_all = pd.concat([df_all, df], ignore_index=True)
    else:   # create it otherwise
        df_all = df

    # Write csv
    df_all.to_csv(file_path)


def list_csv(folder):
    return list_by_extension(folder, extension='.csv')


def list_by_extension(folder, extension='.csv'):
    # List all files
    ls_files = listdir(folder)
    # Check extensions
    ln_ext = len(extension)
    is_csv = []
    for i_ in ls_files:
        if len(i_)>=ln_ext:
            i__ = i_[-ln_ext:]==extension
        else:
            i__ = False
        is_csv.append(i__)
    # Compress list
    ls_files = list( compress(ls_files, is_csv) )
    # Append root
    ls_paths = [path.join(folder, i_) for i_ in ls_files]
    return ls_files, ls_paths
