from random import randint
from typing import Dict, Tuple, Union, Optional


class C:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


def parse_class_name(class_name: str) -> str:
    """
    This will parse a python CamelCase class name and return the resulting strings.
    Example: 'PerfectedStrike' -> 'Perfected Strike'
    """
    final_name = ''
    for char in class_name:
        if char.isupper():
            final_name += ' '
        final_name += char
    return final_name[1:]


def asc_int(ascension: int, value_dict: Dict[int, Union[Tuple[int, int], int]]) -> int:
    """
    Use this to get a value based on ascension
    This will either return a random value between (lower, upper) bounds if a tuple is provided
    Or it will provide a static number if an integer is provided.
    Single static value example: {0: 3} -> For ascension 0+ return 3
    Random Range Example dict: {0: (5, 10)} -> For ascension 1+ random(5, 10)
    NOTE: This is an inclusive bounds
    The value dict provided must be formatted and must include a 0 key to represent no ascension
    ! Warning: Exception will be thrown if there is no 0 key in @value_dict
    ! Warning: Exception will be thrown if the first tuple int is larger than the second
    :param ascension: The ascension you want to generate a number for
    :param value_dict: A dictionary representing ranges by ascension in either of the following formats:
        {$ascension: (lower_bound, upper_bound)} for randomized numbers
        {$ascension: value} for set static numbers
    :return: An integer value based on provided ascension and value dict
    """

    # Start by creating a list of sorted keys
    ascension_bounds = list(value_dict.keys())
    ascension_bounds.sort()

    # We require that there is defined behavior for ascension 1+ at a minimum
    if ascension_bounds[0] != 0:
        raise Exception('Ascension bounds must include a 0 key.')

    # Sub-method to quickly check if this is an int or a random range
    def process_val(index: int) -> int:
        result = value_dict[ascension_bounds[index]]
        if type(result) is tuple:
            if result[0] > result[1]:
                raise Exception()
            else:
                return randint(*result)
        return result

    # Iterate through to try and match the ascension to a range
    for i in range(len(ascension_bounds) - 1):
        if ascension < ascension_bounds[i + 1]:
            return process_val(i)

    # If we still haven't reached it we use the last range
    return process_val(-1)
