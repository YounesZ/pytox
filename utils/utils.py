import pandas as pd
from os import remove
from decimal import Decimal


# ==========================================
# ============= DATA FORMATS ===============
# ==========================================
def convertDatasetToNumeric(df):
    # Convert each data of the dataset into numeric value (ex: NAN from CSV import)
    for c in df.columns:
        df[c] = pd.to_numeric(df[c])
    return df


def decimal_to_numeric(dec, out_type=float):
    if isinstance(dec, Decimal):
        dec = out_type(dec)
    return dec


# ======================================
# ============= FILE OPS ===============
# ======================================
def remove_file(file_path):
    done = False
    try:
        remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
        done = True
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied. Unable to delete file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while deleting file '{file_path}': {str(e)}")
    return done


