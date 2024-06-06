from __future__ import annotations
from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)


class NadaArray(list):
    def __init__(self: NadaArray, *args):
        super().__init__()

        if len(args) == 1 and isinstance(args[0], list):
            argument = args[0]
        elif args and hasattr(args[0], "__iter__") and not isinstance(args[0], (str, list, tuple)):
            # input argument is generator, e.g. NadaArray(i for i in range(5))
            argument = list(args[0])
        else:
            argument = args

        for item in argument:
            self._check_type(item)
            self.append(item)

    @staticmethod
    def _check_type(item: Union[SecretInteger, audit.abstract.SecretInteger]):
        if type(item) not in {SecretInteger, audit.abstract.SecretInteger}:
            raise TypeError(f"all input values must be of type SecretInteger")

    def append(self, item: Union[SecretInteger, audit.abstract.SecretInteger]):
        self._check_type(item)

        super().append(item)

    def extend(self, iterable: Union[NadaArray, List[Union[SecretInteger, audit.abstract.SecretInteger]]]):
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        self._check_type(item)

        super().insert(index, item)

    def __setitem__(self, index, item):
        self._check_type(item)
        super().__setitem__(index, item)
