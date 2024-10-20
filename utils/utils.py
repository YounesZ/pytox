import re
import pandas as pd
from os import remove
from typing import List, Union, Any, Optional
from decimal import Decimal
from .decorators import validate_arguments



# ==========================================
# ============= DATA FORMATS ===============
# ==========================================
@validate_arguments
def remove_chars_and_spaces(input_string: str,
                            chars_to_remove: List[str]):
    pattern = "[" + re.escape("".join(chars_to_remove)) + "\s]"
    result_string = re.sub(pattern, "", input_string)
    return result_string


@validate_arguments
def decimal_to_numeric(dec: Union[Decimal, Any],
                       out_type: Optional[Any] = float) -> Any:
    if isinstance(dec, Decimal):
        dec = out_type(dec)
    return dec


