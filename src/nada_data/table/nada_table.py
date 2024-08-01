from __future__ import annotations
from typing import List, Set, Union
from nada_dsl import audit, Party
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
            self.set_data(rows)

    def __len__(self: NadaTable):
        return len(self._rows)

    def __str__(self: NadaTable) -> str:
        """
        Return a string representation of this NadaTable instance
        """
        cols_str = ",".join(f"'{c}'" for c in self.columns)
        parties_str = ",".join(sorted([f"'{p.name}'" for p in self._parties]))
        return f"NadaTable | cols=[{cols_str}] | rows={len(self._rows)} | parties=[{parties_str}]"

    def __repr__(self: NadaTable) -> str:
        return str(self)

    def __setitem__(self: NadaTable, index: int, row: NadaArray):
        """
        Replace value at :index: of self._rows with :item:
        """

        self._check_input(row)
        self._rows[index] = row
        self._update_parties()

    def __getitem__(self: NadaTable, index: int) -> NadaArray:
        """
        Return value at :index: from self._rows
        """
        return self._rows[index]

    def __delitem__(self: NadaTable, index: int):
        """
        Remove value at :index: from self._rows
        """
        del self._rows[index]
        self._update_parties()

    def _check_input(self: NadaTable, row: NadaArray):
        """
        Determine whether :row: is (1) of NadaArray type, and (2) matches length of self.columns
        """

        if not isinstance(row, NadaArray):
            raise TypeError("rows must be NadaArray instances")
        if len(self.columns) != len(row):
            raise ValueError("input row length must match length of table columns")

    def append(self: NadaTable, row: NadaArray):
        """
        Add a single row to this NadaTable instance
        """

        self._check_input(row)
        self._rows.append(row)
        self._add_parties(row)

    def extend(self: NadaTable, rows: List[NadaArray]):
        """
        Add a list of rows to this NadaTable instance
        """

        for row in rows:
            self._check_input(row)
            self._add_parties(row)
        self._rows.extend(rows)

    def insert(self: NadaTable, index: int, row: NadaArray):
        """
        Insert :row: at :index: of self._rows
        """

        self._check_input(row)
        self._rows.insert(index, row)
        self._add_parties(row)

    def _update_parties(self: NadaTable):
        """
        Update the set of all Party values for this instance
        """
        self._parties = {party for row in self._rows for party in row.get_parties()}

    def _add_parties(self: NadaTable, row: NadaArray):
        """
        Add all Party values for some :item: to this instance
        """
        self._parties = self._parties | row.get_parties()

    def get_parties(self: NadaTable) -> Set[Union[Party, audit.Party]]:
        """
        Return the set of all parties associated with this instance
        """
        return self._parties

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

    def set_data(self: NadaTable, data: List[NadaArray]) -> NadaTable:
        """
        Set the rows parameter for this NadaTable instance
        """
        self._rows = []
        self.extend(data)
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

    def select(self: NadaTable, *cols: str) -> NadaTable:
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

    def concat(self: NadaTable, other: NadaTable) -> NadaTable:
        """
        Return a new NadaTable that is the result of concatenating this instance with another
        """

        if self.columns != other.columns:
            raise ValueError("columns between tables must match to do concat")

        return NadaTable(
            *self.columns,
            rows=self._rows + other._rows
        )

    def sort_by(self: NadaTable, key_col: str, ascending: bool):
        """
        Sort the rows of this table by :key_col: in either ascending or descending order
        """
        odd_even_sort(self._rows, self.get_col_idx(key_col), ascending)

    def aggregate_sum(self: NadaTable, key_col: str, agg_col: str):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_sum(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))

    def aggregate_max(self: NadaTable, key_col: str, agg_col: str):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_max(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))

    def aggregate_min(self: NadaTable, key_col: str, agg_col: str):
        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")
        aggregate_min(self._rows, self.get_col_idx(key_col), self.get_col_idx(agg_col))


def serialize_input_table(
        arrs: List[List[int]], party: audit.Party, prefix: str
) -> List[NadaArray]:
    """
    Construct and return a NadaTable with inputs that match a certain :prefix: and :party:
    ownership. This is intended be used only for testing with the nada_dsl.audit module.
    """
    return [
        NadaArray(
            audit.SecretInteger(
                audit.Input(f"{prefix}{i}_{j}", party=party)
            ) for j in range(len(arrs[i]))
        ) for i in range(len(arrs))
    ]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
