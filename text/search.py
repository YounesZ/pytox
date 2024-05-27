import re
from typing import List
from submodules.pytox.utils.decorators import validate_arguments


@validate_arguments
def contains_pattern(string: str,
                     patterns: List) -> List[bool]:

    # TODO: type regex search patterns

    output = []
    for pattern in patterns:
        if re.search(pattern, string):
            output.append(True)
        else:
            output.append(False)
    return output


@validate_arguments
def list_match_patters(lst: List,
                       patterns: List[str]) -> List[str]:
    matched_strings = [string for string in lst if any(contains_pattern(string, patterns))]
    return matched_strings


@validate_arguments
def remove_pattern(text: str,
                   pattern: str) -> str:
    # Define the pattern to match spaces and underscores
    pattern = rf'[{pattern}]'
    # Replace spaces and underscores with empty string
    result = re.sub(pattern, '', text)
    return result