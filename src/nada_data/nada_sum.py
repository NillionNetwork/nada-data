
from typing import List, Union
from nada_dsl import (
    SecretInteger, PublicInteger, Integer
)
from nada_data.nada_array import NadaArray


def identify_first_element(argument: NadaArray) -> (int, Union[SecretInteger, PublicInteger, Integer]):

    first_public_int: Union[PublicInteger, None] = None
    first_public_int_idx: int = 0
    first_int: Union[Integer, None] = None
    first_int_idx: int = 0

    for i, e in enumerate(argument):
        if isinstance(e, SecretInteger):
            return i, e
        if isinstance(e, PublicInteger) and first_public_int is None:
            first_public_int = e
            first_public_int_idx = i
        if isinstance(e, Integer) and first_int is None:
            first_int = e
            first_int_idx = i

    if first_public_int is not None:
        return first_public_int_idx, first_public_int

    if first_int is not None:
        return first_int_idx, first_int

    return -1, Integer(0)


def nada_sum(
        argument: Union[List[SecretInteger, PublicInteger, Integer, int], NadaArray]
) -> Union[SecretInteger, PublicInteger, Integer]:

    first_element_idx, first_element = identify_first_element(argument)
    output: Union[SecretInteger, PublicInteger, Integer] = first_element

    for i, e in enumerate(argument):
        if i == first_element_idx:
            continue

        if isinstance(e, int):
            e = Integer(e)
        output = output + e

    return output
