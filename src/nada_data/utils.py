"""
Utility functions shared by both the `array` and `table` modules.
"""
from typing import List, Dict
from nada_dsl import audit


def next_power_of_two(n: int) -> int:
    """
    Determine the next power of 2 for some n

    >>> next_power_of_two(2)
    2
    >>> next_power_of_two(37)
    64
    >>> next_power_of_two(-10)
    1

    :param n: Integer to start from
    """

    if n <= 0:
        return 1

    p = 1
    while p < n:
        p <<= 1

    return p


def initialize_array_data(prefix: str, arr: List[int]):
    """
    Initialize an array of data for some prefix

    :param prefix: Prefix string to assign for each input value.
    :param arr: Input list of integers
    """
    audit.Abstract.initialize(
        {f"{prefix}{i}": arr[i] for i in range(len(arr))}
    )


def initialize_array_data_multi(inputs: Dict[str, List[int]]):
    """
    Initialize multiple arrays of input data for some mapping of input party -> array values.

    :param inputs: A dictionary mapping of party names to arrays of integers.
    """
    audit.Abstract.initialize({
        f"{party_name}_{i}": inputs[party_name][i]
        for party_name in inputs.keys()
        for i in range(len(inputs[party_name]))
    })


def initialize_table_data(prefix: str, arrs: List[List[int]]):
    """
    Initialize a two-dimensional array of data for some prefix

    :param prefix: Prefix string to assign for each input value.
    :param arrs: Input list of lists of integers
    """
    audit.Abstract.initialize(
        {f"{prefix}{i}_{j}": val for i, row in enumerate(arrs) for j, val in enumerate(row)}
    )


def initialize_table_data_multi(inputs: Dict[str, List[List[int]]]):
    """
    Initialize multiple tables of input data for some mapping of input party -> table values.

    :param inputs: A dictionary mapping of party names to two-dimensional arrays of integers.
    """
    audit.Abstract.initialize({
        f"{party_name}_{i}_{j}": v
        for party_name, lst in inputs.items()
        for i, sublst in enumerate(lst)
        for j, v in enumerate(sublst)
    })


__all__ = [
    "initialize_array_data", "initialize_table_data",
    "initialize_array_data_multi", "initialize_table_data_multi"
]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
