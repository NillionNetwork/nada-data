from typing import List, Union
from nada_dsl import (
    SecretInteger, PublicInteger, Integer
)
from nada_data.nada_array import NadaArray


def nada_lt(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item < cmp).if_else(item, item - item)


def nada_lteq(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item <= cmp).if_else(item, item - item)


def nada_gt(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item > cmp).if_else(item, item - item)


def nada_gteq(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item >= cmp).if_else(item, item - item)


def nada_eq(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item == cmp).if_else(item, item - item)


def nada_pubeq(
        item: Union[SecretInteger, PublicInteger, Integer],
        cmp: Union[SecretInteger, PublicInteger, Integer]
) -> Union[SecretInteger, PublicInteger, Integer]:
    return (item.public_equals(cmp)).if_else(item, item - item)


def nada_filter(
        argument: Union[List[SecretInteger, PublicInteger, Integer, int], NadaArray],
        op: callable,
        cmp: Union[SecretInteger, PublicInteger, Integer, int]
) -> NadaArray:

    if isinstance(cmp, int):
        cmp = Integer(cmp)

    output = NadaArray()
    for item in argument:
        if isinstance(item, int):
            item = Integer(item)
        output.append(op(item, cmp))
    return output
