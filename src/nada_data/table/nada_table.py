from __future__ import annotations
from typing import List
from nada_data.array.nada_array import NadaArray
from nada_data.table.functions import *


class NadaTable:
    def __init__(
            self: NadaTable,
            *columns: str,
            rows: List[NadaArray] = None
    ):
        self._rows = []
        self._parties = set()
        self.columns = [c for c in columns]
        if rows is not None:
            self._set_data(rows)

    def __str__(self: NadaTable) -> str:
        """
        Return a string representation of this NadaTable instance
        """
        return f"NadaTable | cols={', '.join(c for c in self.columns)} | rows={len(self._rows)}"

    def __repr__(self: NadaTable) -> str:
        return str(self)

    def _set_columns(self: NadaTable, *columns: str):
        for c in columns:
            if not isinstance(c, str):
                raise TypeError("column names must be str")
            if c in self.columns:
                raise ValueError(f"table already contains a column with name '{c}'")
            self.columns.append(c)

    def set_columns(self: NadaTable, *columns: str) -> NadaTable:
        """
        Set the names of the columns for this NadaTable instance. Note that no checking
        is done to ensure that the number of columns matches the number of elements in
        each row of the data for this NadaTable instance.
        """
        self.columns = []
        self._set_columns(*columns)
        return self

    def _set_data(self: NadaTable, data: List[NadaArray]):
        """
        Perform various checks on incoming data for this NadaTable instance.
        """

        for d in data:
            if not isinstance(d, NadaArray):
                raise TypeError("rows must be NadaArray instances")
            if len(d) != len(self.columns):
                raise ValueError("rows must contain the same number of elements as column list")
            self._rows.append(d)
            self._parties = self._parties | d.get_parties()

    def set_data(self: NadaTable, data: List[NadaArray]) -> NadaTable:
        """
        Set the rows parameter for this NadaTable instance
        """
        self._rows = []
        self._set_data(data)
        return self

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
        """

        if not isinstance(row, NadaArray):
            raise TypeError("rows must be NadaArray instances")
        if len(self.columns) != len(row):
            raise ValueError("input row length must match length of table columns")
        self._rows.append(row)

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
                for r in self._rows
            ]
        )

    def sort_by(
            self: NadaTable,
            key_col: str,
            ascending: bool
    ):
        """
        Sort the rows of this table by :key_col: in either ascending or descending order
        """
        odd_even_sort(self._rows, self.get_col_idx(key_col), ascending)

    def aggregate_sum(
            self: NadaTable,
            key_col: str,
            agg_col: str
    ):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_sum(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))

    def aggregate_max(
            self: NadaTable,
            key_col: str,
            agg_col: str
    ):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_max(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))

    def aggregate_min(
            self: NadaTable,
            key_col: str,
            agg_col: str
    ):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_min(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
