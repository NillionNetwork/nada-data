from typing import List, Union, Callable
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.functions.table.sort import odd_even_sort

secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]

FUNCTIONS = {
    "sum": lambda x, y: x + y,
    "max": lambda x, y: (x > y).if_else(x, y),
    "min": lambda x, y: (x < y).if_else(x, y)
}


def _shift_agg(values: List[List[secret_int]], key_col: int, agg_col: int, agg_func: Callable):

    for i in range(len(values) - 1):

        cond = values[i][key_col] == values[i + 1][key_col]
        temp_one = cond.if_else(values[i][agg_col] - values[i][agg_col], values[i][agg_col])
        temp_two = cond.if_else(
            agg_func(values[i][agg_col], values[i + 1][agg_col]),
            values[i + 1][agg_col]
        )

        values[i][agg_col] = temp_one
        values[i + 1][agg_col] = temp_two


def _aggregate(values: List[List[secret_int]], key_col: int, agg_col: int, agg_type: str):

    agg_func = FUNCTIONS.get(agg_type, None)
    if agg_func is None:
        raise ValueError(f"no aggregation function exists with name {agg_type}")
    odd_even_sort(values, key_col, True)
    _shift_agg(values, key_col, agg_col, agg_func)


def aggregate_sum(values: List[List[secret_int]], key_col: int, agg_col: int):
    _aggregate(values, key_col, agg_col, "sum")


def aggregate_max(values: List[List[secret_int]], key_col: int, agg_col: int):
    _aggregate(values, key_col, agg_col, "max")


def aggregate_min(values: List[List[secret_int]], key_col: int, agg_col: int):
    _aggregate(values, key_col, agg_col, "min")
