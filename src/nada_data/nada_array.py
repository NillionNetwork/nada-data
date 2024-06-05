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

