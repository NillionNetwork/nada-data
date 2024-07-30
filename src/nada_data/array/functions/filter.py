from typing import List, Union, Callable
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.array.nada_array import NadaArray


secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


def nada_lt(item: secret_int, cmp: secret_int) -> secret_int:
    return (item < cmp).if_else(item, item - item)


def nada_lteq(item: secret_int, cmp: secret_int) -> secret_int:
    return (item <= cmp).if_else(item, item - item)


def nada_gt(item: secret_int, cmp: secret_int) -> secret_int:
    return (item > cmp).if_else(item, item - item)


def nada_gteq(item: secret_int, cmp: secret_int) -> secret_int:
    return (item >= cmp).if_else(item, item - item)


def nada_eq(item: secret_int, cmp: secret_int) -> secret_int:
    return (item == cmp).if_else(item, item - item)


def filter_nada_array(
        argument: Union[List[secret_int], NadaArray],
        op: Callable[[secret_int, secret_int], secret_int],
        cmp: secret_int
) -> NadaArray:

    output = NadaArray()
    for item in argument:
        output.append(op(item, cmp))
    return output


def nada_max(argument: Union[List[secret_int], NadaArray]) -> secret_int:

    output = argument[0]
    for i in range(1, len(argument)):
        output = (output > argument[i]).if_else(output, argument[i])
    return output


def nada_min(argument: Union[List[secret_int], NadaArray]) -> secret_int:

    output = argument[0]
    for i in range(1, len(argument)):
        output = (output < argument[i]).if_else(output, argument[i])
    return output
