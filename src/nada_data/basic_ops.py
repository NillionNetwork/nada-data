from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)
from nada_data.nada_array import NadaArray


def nada_lt(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item < cmp).if_else(item, item - item)


def nada_lteq(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item <= cmp).if_else(item, item - item)


def nada_gt(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item > cmp).if_else(item, item - item)


def nada_gteq(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item >= cmp).if_else(item, item - item)


def nada_eq(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item == cmp).if_else(item, item - item)


def nada_pubeq(
        item: Union[SecretInteger, audit.abstract.SecretInteger],
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:
    return (item.public_equals(cmp)).if_else(item, item - item)


def nada_filter(
        argument: Union[List[Union[SecretInteger, audit.abstract.SecretInteger]], NadaArray],
        op: callable,
        cmp: Union[SecretInteger, audit.abstract.SecretInteger]
) -> NadaArray:

    output = NadaArray()
    for item in argument:
        output.append(op(item, cmp))
    return output


def nada_sum(
        argument: Union[List[Union[SecretInteger, audit.abstract.SecretInteger]], NadaArray]
) -> Union[SecretInteger, audit.abstract.SecretInteger]:

    output = argument[0]
    for e in argument[1:]:
        if type(e) not in {SecretInteger, audit.abstract.SecretInteger}:
            raise TypeError(f"all input values must be of type SecretInteger")
        output = output + e

    return output
