from __future__ import annotations
from typing import List
from nada_dsl import SecretInteger
from nada_data.nada_array import NadaArray


class NadaTable:
    def __init__(
            self: NadaTable,
            *columns: str,
            rows: List[NadaArray] = None
    ):

        self.columns = [c for c in columns]
        self.rows = self._set_data(rows) if rows is not None else []

    def __str__(self: NadaTable) -> str:
        """
        Return a string representation of this NadaTable instance

        >>> arrs = [NadaArray(SecretInteger(i) for i in range(2)), NadaArray(SecretInteger(i + 5) for i in range(2))]
        >>> NadaTable('a', 'b', rows=arrs)
        NadaTable(a, b)
        """
        return f"NadaTable({', '.join([c for c in self.columns])})"

    def __repr__(self: NadaTable) -> str:
        return str(self)

    def set_columns(self: NadaTable, *columns: str) -> NadaTable:
        """
        Set the names of the columns for this NadaTable instance. Note that no checking
        is done to ensure that the number of columns matches the number of elements in
        each row of the data for this NadaTable instance.

        >>> arrs = [NadaArray(SecretInteger(i) for i in range(2)), NadaArray(SecretInteger(i + 5) for i in range(2))]
        >>> nt = NadaTable('a', 'b', rows=arrs)
        >>> nt.set_columns('c', 'd')
        NadaTable(c, d)
        """

        self.columns = []
        for c in columns:
            if not isinstance(c, str):
                raise TypeError("column names must be str")
            if c in self.columns:
                raise ValueError(f"table already contains a column with name '{c}'")
            self.columns.append(c)

        return self

    def _set_data(self: NadaTable, data: List[NadaArray]) -> List[NadaArray]:
        """
        Perform various checks on incoming data for this NadaTable instance.

        >>> nt = NadaTable('a', 'b')
        >>> arrs = [NadaArray(SecretInteger(i) for i in range(2)), NadaArray(SecretInteger(i + 5) for i in range(2))]
        >>> nt._set_data(arrs)
        [NadaArray(0, 1), NadaArray(5, 6)]

        The number of elements in each row of the incoming data should match the existing number of columns for
        this instance:
        >>> nt = NadaTable('a', 'b')
        >>> arrs = [NadaArray(SecretInteger(i) for i in range(2)), NadaArray(SecretInteger(i + 5) for i in range(3))]
        >>> nt._set_data(arrs)
        Traceback (most recent call last):
          ...
        ValueError: rows must contain the same number of elements as column list

        All incoming rows should be of type NadaArray:
        >>> nt = NadaTable('a', 'b')
        >>> nt._set_data([[i for i in range(2)]])
        Traceback (most recent call last):
          ...
        TypeError: rows must be NadaArray instances
        """

        for d in data:
            if not isinstance(d, NadaArray):
                raise TypeError("rows must be NadaArray instances")
            if len(d) != len(self.columns):
                raise ValueError("rows must contain the same number of elements as column list")
        return data

    def set_data(self: NadaTable, data: List[NadaArray]) -> NadaTable:
        """
        Set the rows parameter for this NadaTable instance

        >>> nt = NadaTable('a', 'b')
        >>> arrs = [NadaArray(SecretInteger(i) for i in range(2)), NadaArray(SecretInteger(i + 5) for i in range(2))]
        >>> nt.set_data(arrs)
        >>> nt.rows
        [NadaArray(0, 1), NadaArray(5, 6)]
        """
        self.rows = self._set_data(data)

    def get_col_idx(self: NadaTable, col_name: str) -> int:
        """
        Get the integer idx for the column with name :col_name:

        >>> nt = NadaTable('a', 'b')
        >>> nt.get_col_idx('b')
        1
        """
        try:
            return self.columns.index(col_name)
        except ValueError:
            raise ValueError(f"column {col_name} not in {self}")

    def add_row(self: NadaTable, row: NadaArray):
        """
        Add a single row to this NadaTable instance

        >>> nt = NadaTable('a', 'b')
        >>> nt.add_row(NadaArray(SecretInteger(i) for i in range(2)))
        >>> nt.rows
        [NadaArray(0, 1)]

        >>> nt = NadaTable('a', 'b')
        >>> nt.add_row([SecretInteger(i) for i in range(2)])
        Traceback (most recent call last):
          ...
        TypeError: rows must be NadaArray instances

        >>> nt = NadaTable('a', 'b')
        >>> nt.add_row(NadaArray(SecretInteger(i) for i in range(3)))
        Traceback (most recent call last):
          ...
        ValueError: input row length must match length of table columns
        """

        if not isinstance(row, NadaArray):
            raise TypeError("rows must be NadaArray instances")
        if len(self.columns) != len(row):
            raise ValueError("input row length must match length of table columns")
        self.rows.append(row)

    def select(
            self: NadaTable,
            *cols: str
    ) -> NadaTable:
        """
        Perform basic select operation on this table, returning a new NadaTable with rows
        consisting of only the specified :cols:
        """
        return NadaTable(
            *cols,
            rows=[
                NadaArray(r[i] for i in [self.columns.index(c) for c in cols])
                for r in self.rows
            ]
        )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
