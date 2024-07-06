from __future__ import annotations
import inspect
from typing import List, Union
from nada_dsl import (
    SecretInteger, audit
)


secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


class NadaArray(list):
    """
    Data structure for representing arrays of SecretIntegers. The constructor accepts
    tuples, lists, and generators and parses them accordingly.

    >>> NadaArray([SecretInteger(1), SecretInteger(2)])
    NadaArray(1, 2)
    >>> NadaArray(SecretInteger(i) for i in range(5))
    NadaArray(0, 1, 2, 3, 4)
    >>> NadaArray(SecretInteger(1), SecretInteger(2))
    NadaArray(1, 2)
    >>> NadaArray(5)
    Traceback (most recent call last):
      ...
    TypeError: all array values must be of type SecretInteger
    """
    def __init__(self: NadaArray, *args):
        super().__init__()

        if len(args) == 1:
            if isinstance(args[0], list):
                args = args[0]
            if inspect.isgenerator(args[0]):
                args = list(args[0])

        for item in args:
            self._check_type(item)
            self.append(item)

    def __str__(self):
        """
        Return a string representation of this instance.

        >>> NadaArray(SecretInteger(5), SecretInteger(4))
        NadaArray(5, 4)
        """
        return f"NadaArray({', '.join([str(i.inner) for i in self])})"

    def __repr__(self):
        """
        Return a string representation of this instance.
        """
        return str(self)

    def __add__(self, other: Union[NadaArray, List[secret_int]]):
        """
        Concatenate this instance with another NadaArray or list of SecretInteger instances

        >>> NadaArray(SecretInteger(1), SecretInteger(2)) + NadaArray(SecretInteger(3), SecretInteger(4))
        NadaArray(1, 2, 3, 4)
        >>> NadaArray(SecretInteger(1), SecretInteger(2)) + [SecretInteger(3), SecretInteger(4)]
        NadaArray(1, 2, 3, 4)
        """
        return NadaArray([i for i in self] + [i for i in other])

    @staticmethod
    def _check_type(item: secret_int):
        """
        Determine whether :item: is of SecretInteger type

        >>> NadaArray._check_type(SecretInteger(5))
        >>> NadaArray._check_type("Hello")
        Traceback (most recent call last):
          ...
        TypeError: all array values must be of type SecretInteger
        >>> NadaArray._check_type(5)
        Traceback (most recent call last):
          ...
        TypeError: all array values must be of type SecretInteger
        """
        if type(item) not in secret_int_types:
            raise TypeError(f"all array values must be of type SecretInteger")

    def append(self, item: secret_int):
        """
        Append :item: to this instance

        >>> arr = NadaArray(SecretInteger(5))
        >>> arr.append(SecretInteger(6))
        >>> arr
        NadaArray(5, 6)
        """
        self._check_type(item)
        super().append(item)

    def extend(self, iterable: Union[NadaArray, List[secret_int]]):
        """
        Extend this instance with an iterable

        >>> arr1 = NadaArray(SecretInteger(5), SecretInteger(6))
        >>> arr2  = NadaArray([SecretInteger(1), SecretInteger(2)])
        >>> arr1.extend(arr2)
        >>> arr1
        NadaArray(5, 6, 1, 2)
        """
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        """
        Insert :item: into this instance at index :index:

        >>> arr = NadaArray(SecretInteger(5), SecretInteger(6))
        >>> arr.insert(0, SecretInteger(2))
        >>> arr
        NadaArray(2, 5, 6)
        >>> arr.insert(10, SecretInteger(2))
        >>> arr
        NadaArray(2, 5, 6, 2)
        """
        self._check_type(item)
        super().insert(index, item)

    def __setitem__(self, index, item):
        """
        Replace value at :index: with :item:
        >>> arr = NadaArray(SecretInteger(5), SecretInteger(6))
        >>> arr[0] = SecretInteger(1)
        >>> arr
        NadaArray(1, 6)
        """
        self._check_type(item)
        super().__setitem__(index, item)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
