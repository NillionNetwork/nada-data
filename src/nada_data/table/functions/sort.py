from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)
from nada_data import utils

secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


def _compare_exchange(
        values: List[List[secret_int]], key_col: int, ascending: bool, i: int, j: int
):

    if i >= len(values) or j >= len(values):
        return

    x = values[i][key_col]
    y = values[j][key_col]

    cond = x < y
    for k in range(len(values[i])):
        temp_one = cond.if_else(values[i][k], values[j][k])
        temp_two = cond.if_else(values[j][k], values[i][k])

        if ascending:
            values[i][k] = temp_one
            values[j][k] = temp_two
        else:
            values[i][k] = temp_two
            values[j][k] = temp_one


def _odd_even_merge(
        values: List[List[secret_int]], key_col: int, ascending: bool, lo: int, n: int, r: int
):

    m = r * 2
    if m < n:

        _odd_even_merge(values, key_col, ascending, lo, n, m)
        _odd_even_merge(values, key_col, ascending, lo + r, n, m)

        i = lo + r
        while (i + r) < (lo + n):
            _compare_exchange(values, key_col, ascending, i, i + r)
            i += m
    else:
        _compare_exchange(values, key_col, ascending, lo, lo + r)


def _odd_even_sort(
        values: List[List[secret_int]], key_col: int, ascending: bool, lo: int, n: int
):
    if n > 1:
        m = int(n / 2)
        _odd_even_sort(values, key_col, ascending, lo, m)
        _odd_even_sort(values, key_col, ascending, lo + m, m)
        _odd_even_merge(values, key_col, ascending, lo, n, 1)


def odd_even_sort(
        values: List[List[secret_int]], key_col: int, ascending: bool
):
    _odd_even_sort(values, key_col, ascending, 0, utils.next_power_of_two(len(values)))
