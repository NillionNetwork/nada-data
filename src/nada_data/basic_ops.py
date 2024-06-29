from typing import List, Union, Callable
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.nada_array import NadaArray


secret_int_types = {SecretInteger, audit.abstract.SecretInteger}
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


def nada_filter(
        argument: Union[List[secret_int], NadaArray],
        op: Callable[[secret_int, secret_int], secret_int],
        cmp: secret_int
) -> NadaArray:

    output = NadaArray()
    for item in argument:
        output.append(op(item, cmp))
    return output


def nada_sum(argument: Union[List[secret_int], NadaArray]) -> secret_int:
    """
    Sum an array of SecretInteger objects
    """

    output = argument[0]
    for e in argument[1:]:
        if type(e) not in secret_int_types:
            raise TypeError(f"all input values must be of type SecretInteger")
        output = output + e

    return output


if __name__ == "__main__":
    import doctest
    doctest.testmod()