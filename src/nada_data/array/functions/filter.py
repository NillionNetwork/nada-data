"""
Filter functions for use with NadaArray instances
"""
from typing import List, Union, Callable
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.array.nada_array import NadaArray


secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


def nada_lt(item: secret_int, cmp: secret_int) -> secret_int:
    """
    If **item** is less than **cmp**, return it. Else, return 0.

    :param item: Left input value.
    :param cmp: Right input value.
    """
    return (item < cmp).if_else(item, item - item)


def nada_lteq(item: secret_int, cmp: secret_int) -> secret_int:
    """
    If **item** is less than or equal to **cmp**, return it. Else, return 0.

    :param item: Left input value.
    :param cmp: Right input value.
    """
    return (item <= cmp).if_else(item, item - item)


def nada_gt(item: secret_int, cmp: secret_int) -> secret_int:
    """
    If **item** is greater than **cmp**, return it. Else, return 0.

    :param item: Left input value.
    :param cmp: Right input value.
    """
    return (item > cmp).if_else(item, item - item)


def nada_gteq(item: secret_int, cmp: secret_int) -> secret_int:
    """
    If **item** is greater than or equal to **cmp**, return it. Else, return 0.

    :param item: Left input value.
    :param cmp: Right input value.
    """
    return (item >= cmp).if_else(item, item - item)


def nada_eq(item: secret_int, cmp: secret_int) -> secret_int:
    """
    If **item** is equal to **cmp**, return it. Else, return 0.

    :param item: Left input value.
    :param cmp: Right input value.
    """
    return (item == cmp).if_else(item, item - item)


def filter_nada_array(
        argument: Union[List[secret_int], NadaArray],
        op: Callable[[secret_int, secret_int], secret_int],
        cmp: secret_int
) -> NadaArray:
    """
    Filter a NadaArray against (1) some callable that accepts two secret_int
    instances and returns a secret int and (2) a secret_int to compare against
    each element of the input NadaArray.

    :param argument: Input array
    :param op: Callable that accepts two SecretInteger instances, and returns a SecretInteger
    :param cmp: A SecretInteger to compare against each element of the input NadaArray
    """

    output = NadaArray()
    for item in argument:
        output.append(op(item, cmp))
    return output


def nada_max(argument: Union[List[secret_int], NadaArray]) -> secret_int:
    """
    Return the maximum value in the input array

    :param argument: Input array
    """

    output = argument[0]
    for i in range(1, len(argument)):
        output = (output > argument[i]).if_else(output, argument[i])
    return output


def nada_min(argument: Union[List[secret_int], NadaArray]) -> secret_int:
    """
    Return the minimum value in the input array

    :param argument: Input array
    """

    output = argument[0]
    for i in range(1, len(argument)):
        output = (output < argument[i]).if_else(output, argument[i])
    return output
