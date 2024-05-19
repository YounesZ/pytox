import re
from typing import List


def contains_pattern(string: str,
                     patterns: str) -> bool:

    # TODO: type regex search patterns

    for pattern in patterns:
        if re.search(pattern, string):
            return True
    return False


def list_match_patters(lst: List,
                       patterns: List[str]) -> List[str]:
    matched_strings = [string for string in lst if contains_pattern(string, patterns)]
    return matched_strings


def remove_pattern(text: str,
                   pattern: str) -> str:
    # Define the pattern to match spaces and underscores
    pattern = rf'[{pattern}]'
    # Replace spaces and underscores with empty string
    result = re.sub(pattern, '', text)
    return result