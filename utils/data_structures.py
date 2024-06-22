import numpy as np
import pandas as pd
from os import path, listdir
from typing import Any, List, Tuple, Optional, Union, Dict
from random import shuffle
from inspect import stack
from .time_stamps import get_last_week_date
from itertools import compress
from submodules.pytox.utils.decorators import validate_arguments



# ==========================================
# ============ DATA STRUCTURES =============
# ==========================================
@validate_arguments
def replicate_until(obj: Union[List, pd.DataFrame],
                    n: int,
                    shuffle: bool = False) -> Any:

    # Check for type
    if isinstance(obj, list):
        obj = _replicate_list_until(obj, n, shuffle)
    elif isinstance(obj, pd.DataFrame):
        obj = _replicate_df_until(obj, n, shuffle)

     # Cut to right length
    obj = obj[:n]
    return obj


# ========================================
# ============ STRING CHAINS =============
# ========================================
@validate_arguments
def capitalize_first(string: str) -> str:

    assert isinstance(string, str)

    string_C = string
    if len(string)>0:
        string_C = string[0].upper() + string[1:].lower()
    return string_C


@validate_arguments
def remove_from_string(string: str,
                       torem: Union[List[str], str]) -> str:

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


# ======================================
# =========== DICTIONARIES =============
# ======================================
@validate_arguments
def serialize_dictionary(criteria: Dict) -> str:
    output = ''
    for i_ in criteria.keys():
        suffix = '-'.join([str(j_) for j_ in criteria[i_]])
        output += '%s--%s__' % (i_, suffix)
    output = output[:-2]
    return output


@validate_arguments
def flip_dict(dico: Dict) -> Dict:
    flipped = {}
    for k, v in dico.items():
        for i_ in v:
            flipped.update({i_: k})
    return flipped


# ======================================
# =========== PYTHON LISTS =============
# ======================================
@validate_arguments
def _replicate_list_until(ls: List,
                          n: int,
                          do_shuffle: bool) -> List:
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


@validate_arguments
def is_list_of_strings(lst: List) -> bool:
    # Determine elements types
    is_str = [isinstance(i_, str) for i_ in lst]
    if all(is_str):
        return True
    else:
        return False


@validate_arguments
def get_index_in_ordered_list(objval: float,
                              vallist: List[Union[int, float]]) -> int:
    # Check if object has a spot
    ix = None
    if objval < max(vallist):
        # Get insertion index
        nvalues = vallist + [objval]
        nvalues.sort()
        ix = nvalues.index(objval)
    return ix


def sorted_indices(lst: List) -> List:
    idx = [i[0] for i in sorted(enumerate(lst), key=lambda x: x[1])]
    idx = idx[::-1]
    return idx


# =======================================
# =========== PANDAS SERIES =============
# =======================================
def sample_as_distribution(srs: pd.Series,
                           n_values: int,
                           default_value: Optional[Any] = None) -> List:

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


def _replicate_df_until(df: pd.DataFrame,
                        n: int,
                        shuffle: bool) -> pd.DataFrame:

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
def append_csv(df: pd.DataFrame,
               file_path: str) -> None:

    # TODO: type filepath

    # If the file exists already, append data
    if path.isfile(file_path):
        # Load file
        df_all = pd.read_csv(file_path, index_col=False)
        # Concatenate dataframes
        df_all = pd.concat([df_all, df], ignore_index=True)
    else:   # create it otherwise
        df_all = df

    # Write csv
    df_all.to_csv(file_path, index=False)


def list_csv(folder: str) -> Tuple[List[str], List[str]]:
    # TODO: type folder
    return list_by_extension(folder, extension='.csv')


def list_by_extension(folder: str,
                      extension: str = '.csv') -> Tuple[List[str], List[str]]:

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
