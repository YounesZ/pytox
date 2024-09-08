import pandas as pd
from typing import List


def update_row_with_columns_from_df(row: pd.Series, columns: List[str], auxiliary: pd.DataFrame):
    # Create a tuple key from the index or unique identifier
    key = row.name

    if key in auxiliary.index:
        # If the key exists in auxiliary, update the row with the values from auxiliary
        row[columns] = auxiliary.loc[key, columns].values[0]

    return row