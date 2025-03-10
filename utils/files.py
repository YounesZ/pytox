import os
from shutil import rmtree
from typing import List, Optional
from datetime import datetime
from itertools import compress



# =============================== #
# ---       LIST FILES        --- #
# =============================== #
def list_csv(folder):
    # List all files
    ls_files = os.listdir(folder)
    # Check extensions
    is_csv = []
    for i_ in ls_files:
        if len(i_)>=4:
            i__ = i_[-4:]=='.csv'
        is_csv.append(i__)
    # Compress list
    ls_files = list( compress(ls_files, is_csv) )
    return ls_files


def list_files_with_extension(folder: str,
                              extension: str) -> List[str]:

    # List all files
    ls_files = os.listdir(folder)

    # Filter with extension
    nchar = len(extension)
    filtr = [i_[-nchar:]==extension for i_ in ls_files]
    ls_files = list( compress(ls_files, filtr) )
    return ls_files


def list_files_with_date(min_date: datetime,
                         max_date: datetime,
                         region: Optional[str] = None,
                         scraper: Optional[str] = None,
                         folder: str = ''):

    # List all files in data folder
    ls_files = list_files_with_extension(folder, '.csv')

    # Split file name
    ls_regions = [i_.split('_')[0] if i_.count('_')==3 else 'other' for i_ in ls_files]
    ls_scrapers = [i_.split('_')[1] if i_.count('_') == 3 else 'other' for i_ in ls_files]
    ls_dates = [i_.split('_')[2] if i_.count('_')==3 else '21000101' for i_ in ls_files]

    # --- Filter with dates
    # Format dates
    ls_dates = [datetime(year=int(i_[:4]), month=int(i_[4:6]), day=int(i_[6:8])) for i_ in ls_dates]

    # Filter dates
    fltr_files = [(i_<=max_date) & (i_>=min_date) for i_ in ls_dates]

    # --- Filter with region
    if not region is None:
        fltr_files = [j_ & (i_ == region) for i_, j_ in zip(ls_regions, fltr_files)]

    if not scraper is None:
        fltr_files = [j_ & (i_ == scraper) for i_, j_ in zip(ls_scrapers, fltr_files)]

    ok_files = [i_ for i_, j_ in zip(ls_files, fltr_files) if j_]

    return ok_files




# =============================== #
# ---         Folders         --- #
# =============================== #
def remove_folder_contents(folder_path: str) -> None:

    # TODO: type folder

    # Iterate over all files and subfolders in the given folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file and remove it
        if os.path.isfile(item_path):
            os.remove(item_path)

        # If the item is a directory, recursively remove its contents
        elif os.path.isdir(item_path):
            rmtree(item_path)


def create_folder(folder_path: str) -> None:
    # Check if the folder does not exist
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def remove_file(file_path: str) -> None:
    done = False
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
        done = True
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied. Unable to delete file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while deleting file '{file_path}': {str(e)}")
    return done
