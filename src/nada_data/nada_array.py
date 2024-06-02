from __future__ import annotations
from typing import List, Union
from nada_dsl import (
    SecretInteger, PublicInteger, Integer
)


class NadaArray(list):
    def __init__(self: NadaArray, *args):
        super().__init__()

        if len(args) == 1 and isinstance(args[0], list):
            argument = args[0]
        else:
            argument = args

        for item in argument:
            self._check_type(item)
            if isinstance(item, int):
                item = Integer(item)
            self.append(item)

    @staticmethod
    def _check_type(item: Union[SecretInteger, PublicInteger, Integer]):
        if type(item) not in {SecretInteger, PublicInteger, Integer}:
            raise TypeError(
                "supplied items must be of the following types: {SecretInteger, PublicInteger, Integer, int}"
            )

    def append(self, item: Union[SecretInteger, PublicInteger, Integer, int]):

        if isinstance(item, int):
            item = Integer(item)
        self._check_type(item)

        super().append(item)

    def extend(self, iterable: Union[NadaArray, List[Union[SecretInteger, PublicInteger, Integer, int]]]):
        for item in iterable:
            self.append(item)

    def insert(self, index, item):

        if isinstance(item, int):
            item = Integer(item)
        self._check_type(item)

        super().insert(index, item)

    def __setitem__(self, index, item):

        if isinstance(item, int):
            item = Integer(item)
        self._check_type(item)

        super().__setitem__(index, item)

    def sum(self) -> Union[SecretInteger, PublicInteger, Integer]:

        first_element_idx, first_element = identify_first_element(self)
        output: Union[SecretInteger, PublicInteger, Integer] = first_element

        for i, e in enumerate(self):
            if i == first_element_idx:
                continue

            if isinstance(e, int):
                e = Integer(e)
            output = output + e

        return output


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
