from __future__ import annotations
from typing import List, Union
from nada_dsl import (
    SecretInteger, PublicInteger, Integer, audit
)


nada_numeric_types = {
    SecretInteger, audit.abstract.SecretInteger,
    PublicInteger, audit.abstract.PublicInteger,
}


class NadaArray(list):
    def __init__(self: NadaArray, *args):
        super().__init__()

        # input argument is list
        if len(args) == 1 and isinstance(args[0], list):
            argument = args[0]
        # input argument is generator, e.g. NadaArray(i for i in range(5))
        elif args and hasattr(args[0], "__iter__") and not isinstance(args[0], (str, list, tuple)):
            argument = list(args[0])
        else:
            argument = args

        for item in argument:
            self._check_type(item)
            self.append(item)

    @staticmethod
    def _check_type(item: Union[*nada_numeric_types]):
        if type(item) not in nada_numeric_types:
            raise TypeError(
                f"supplied items must be of the following types: {nada_numeric_types}"
            )

    def append(self, item: Union[*nada_numeric_types]):
        self._check_type(item)

        super().append(item)

    def extend(self, iterable: Union[NadaArray, List[Union[*nada_numeric_types]]]):
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        self._check_type(item)

        super().insert(index, item)

    def __setitem__(self, index, item):
        self._check_type(item)
        super().__setitem__(index, item)
