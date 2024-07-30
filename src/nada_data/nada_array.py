from __future__ import annotations
import inspect
from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)


secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


class NadaArray:
    """
    Data structure for representing arrays of SecretIntegers. The constructor accepts
    tuples, lists, and generators and parses them accordingly.
    """
    def __init__(self: NadaArray, *args):

        self.data = []
        self._parties = set()

        if len(args) == 1:
            if isinstance(args[0], list):
                args = args[0]
            if inspect.isgenerator(args[0]):
                args = list(args[0])

        for item in args:
            self.append(item)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        """
        Return a string representation of this instance.
        """
        parties_str = ", ".join(sorted([f"'{p.name}'" for p in self._parties]))
        return f"NadaArray | len={len(self.data)} | parties=[{parties_str}]"

    def __repr__(self):
        """
        Return a string representation of this instance.
        """
        return str(self)

    def __add__(self, other: Union[NadaArray, List[secret_int]]):
        """
        Concatenate this instance with another NadaArray or list of SecretInteger instances
        """
        return NadaArray(self.data + other.data)

    @staticmethod
    def _check_type(item: secret_int):
        """
        Determine whether :item: is of SecretInteger type
        """
        if type(item) not in secret_int_types:
            raise TypeError(f"all array values must be of type SecretInteger")

    def append(self, item: secret_int):
        """
        Append :item: to this instance
        """

        self._check_type(item)
        self.data.append(item)
        self.add_parties(item)

    def extend(self, iterable: Union[NadaArray, List[secret_int]]):
        """
        Extend this instance with an iterable
        """

        for item in iterable:
            self._check_type(item)
            self.add_parties(item)
        self.data.extend(iterable)

    def update_parties(self):
        """
        Update the set of all Party values for this instance
        """
        return {party for obj in self for party in obj.parties}

    def add_parties(self, item: secret_int):
        """
        Add all Party values for some :item: to this instance
        """
        for party in item.parties:
            self._parties.add(party)

    def insert(self, index: int, item: secret_int):
        """
        Replace value at :index: with :item:. If :index: is larger than the number of
        elements in self.data, then :item: is appended to self.data.
        """

        self._check_type(item)
        self.data.insert(index, item)
        self.add_parties(item)

    def __setitem__(self, index: int, item: secret_int):
        """
        Replace value at :index: of self.data with :item:
        """

        self._check_type(item)
        self.data[index] = item
        self.update_parties()

    def __getitem__(self, index: int):
        """
        Return value at :index: from self.data
        """
        return self.data[index]
