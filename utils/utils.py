import re
import pandas as pd
from os import remove
from typing import List, Union, Any, Optional
from decimal import Decimal


# =====================================
# ============= STRINGS ===============
# =====================================
def remove_chars_and_spaces(input_string: str,
                            chars_to_remove: str) -> str:

    pattern = "[" + re.escape("".join(chars_to_remove)) + "\s]"
    result_string = re.sub(pattern, "", input_string)
    return result_string


# ==========================================
# ============= DATA FORMATS ===============
# ==========================================
def convertDatasetToNumeric(df: pd.DataFrame) -> pd.DataFrame:
    # Convert each data of the dataset into numeric value (ex: NAN from CSV import)
    for c in df.columns:
        df[c] = pd.to_numeric(df[c])
    return df


def decimal_to_numeric(dec: Union[Decimal, Any],
                       out_type: Optional[Any] = float) -> Any:
    if isinstance(dec, Decimal):
        dec = out_type(dec)
    return dec


# ======================================
# ============= FILE OPS ===============
# ======================================
def remove_file(file_path: str) -> bool:

    # TODO: type filepath
    
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


