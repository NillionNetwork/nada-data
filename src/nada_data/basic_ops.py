from typing import List, Union
from nada_dsl import (
    SecretInteger, PublicInteger, Integer, audit
)
from nada_data.nada_array import NadaArray


nada_numeric_types = {
    SecretInteger, audit.abstract.SecretInteger,
    PublicInteger, audit.abstract.PublicInteger,
}


def nada_lt(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item < cmp).if_else(item, item - item)


def nada_lteq(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item <= cmp).if_else(item, item - item)


def nada_gt(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item > cmp).if_else(item, item - item)


def nada_gteq(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item >= cmp).if_else(item, item - item)


def nada_eq(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item == cmp).if_else(item, item - item)


def nada_pubeq(
        item: Union[*nada_numeric_types],
        cmp: Union[*nada_numeric_types]
) -> Union[*nada_numeric_types]:
    return (item.public_equals(cmp)).if_else(item, item - item)


def nada_filter(
        argument: Union[List[Union[*nada_numeric_types]], NadaArray],
        op: callable,
        cmp: Union[*nada_numeric_types]
) -> NadaArray:

    if isinstance(cmp, int):
        cmp = Integer(cmp)

    output = NadaArray()
    for item in argument:
        if isinstance(item, int):
            item = Integer(item)
        output.append(op(item, cmp))
    return output


def nada_sum(
        argument: Union[List[Union[*nada_numeric_types]], NadaArray]
) -> Union[*nada_numeric_types]:

    output = argument[0]
    for e in argument[1:]:
        if type(e) not in nada_numeric_types:
            raise TypeError(f"all input values must be of the following types: {nada_numeric_types}")
        output = output + e

    return output
