import pandas as pd
from os import path
from .utils import convertDatasetToNumeric


def load_datafile(file_name: str ='ClutchEngagment_FullDataset.csv',
                  force_numeric: bool = True,
                  separator: str =';',
                  decimal: str =',',
                  path_to_assets: str ='') -> pd.DataFrame:

    # Get file type
    file_path = path.join(path_to_assets, 'raw', file_name)
    # Loading
    if file_name[-4:]=='.csv':      # use csv loader
        file_load = pd.read_csv(file_path, sep=separator, decimal=decimal, encoding='latin1')
    elif file_name[-4:]=='.pkl':    # use pkl loader
        file_load = pd.read_pickle(file_path)
    # Convert data
    if force_numeric:
        file_load = convertDatasetToNumeric(file_load)
    return file_load