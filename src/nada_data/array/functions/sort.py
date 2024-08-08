"""
Sorting functions for use with NadaArray instances
"""
from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)
from nada_data import utils

secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


def _compare_exchange(values: List[secret_int], ascending: bool, i: int, j: int):

    if i >= len(values) or j >= len(values):
        return

    x = values[i]
    y = values[j]

    c = (x < y).if_else(x, y)
    d = (x > y).if_else(x, y)

    if ascending:
        values[i] = c
        values[j] = d
    else:
        values[i] = d
        values[j] = c


def _odd_even_merge(values: List[secret_int], ascending: bool, lo: int, n: int, r: int):

    m = r * 2
    if m < n:

        _odd_even_merge(values, ascending, lo, n, m)
        _odd_even_merge(values, ascending, lo + r, n, m)

        i = lo + r
        while (i + r) < (lo + n):
            _compare_exchange(values, ascending, i, i + r)
            i += m
    else:
        _compare_exchange(values, ascending, lo, lo + r)


def _odd_even_sort(values: List[secret_int], ascending: bool, lo: int, n: int):
    if n > 1:
        m = int(n / 2)
        _odd_even_sort(values, ascending, lo, m)
        _odd_even_sort(values, ascending, lo + m, m)
        _odd_even_merge(values, ascending, lo, n, 1)


def sort_nada_array(
        values: List[secret_int], ascending: bool = True
) -> List[secret_int]:
    """
    Sort the contents of **values** in either ascending or descending order

    :param values: Input array
    :param ascending: Control ordering on sorted output
    """
    _odd_even_sort(values, ascending, 0, utils.next_power_of_two(len(values)))
    return values
