"""
Defines the NadaTable class
"""
from __future__ import annotations
import copy
from typing import List, Set, Union, Callable
from nada_dsl import audit, Party, SecretInteger
from nada_data.array.nada_array import NadaArray
from nada_data.table import functions


secret_int_types = {SecretInteger, audit.SecretInteger}
secret_int = Union[*secret_int_types]


class NadaTable:
    """
    Data structure for representing tables of NadaArray instances. The constructor accepts
    a comma-separated list of column names along with a list of NadaArray instances.
    """
    def __init__(
            self: NadaTable,
            *columns: str,
            rows: List[NadaArray] = None
    ):
        self._rows = []
        self._parties = set()
        self.columns = list(columns)
        if rows is not None:
            self.set_data(rows)

    def __len__(self: NadaTable):
        return len(self._rows)

    def __str__(self: NadaTable) -> str:

        cols_str = ",".join(f"'{c}'" for c in self.columns)
        parties_str = ",".join(sorted([f"'{p}'" for p in self._parties]))
        return f"NadaTable | cols=[{cols_str}] | rows={len(self._rows)} | parties=[{parties_str}]"

    def __repr__(self: NadaTable) -> str:
        return str(self)

    def __setitem__(self: NadaTable, index: int, row: NadaArray):

        self._check_input(row)
        self._rows[index] = row
        self._update_parties()

    def __getitem__(self: NadaTable, index: int) -> NadaArray:
        return self._rows[index]

    def __delitem__(self: NadaTable, index: int):
        del self._rows[index]
        self._update_parties()

    def _check_input(self: NadaTable, row: NadaArray):
        """
        Determine whether **row** is (1) of NadaArray type, and (2) matches length of self.columns
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
        Insert **row** at **index** of self._rows
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
        Add all Party values for some **item** to this instance
        """
        self._parties = self._parties | row.get_parties()

    def get_parties(self: NadaTable) -> Set[Union[Party, audit.Party]]:
        """
        Return the set of all input parties associated with the data stored by this instance
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

        :param columns: Variadic argument for the names of this instance's columns
        """

        self.columns = []
        self._set_columns(*columns)
        return self

    def set_data(self: NadaTable, data: List[NadaArray]) -> NadaTable:
        """
        Set the rows parameter for this NadaTable instance

        :param data: List of NadaArray instances
        """
        self._rows = []
        self.extend(data)
        return self

    def get_data(self) -> List[NadaArray]:
        """
        Get the rows from this instance
        """
        return self._rows

    def get_col_idx(self: NadaTable, col_name: str) -> int:
        """
        Get the integer idx for the column with name **col_name**

        >>> nt = NadaTable('a', 'b')
        >>> nt.get_col_idx('b')
        1

        :param col_name: The name of the column to obtain the index of
        """
        try:
            return self.columns.index(col_name)
        except ValueError as exc:
            raise ValueError(f"column {col_name} not in {self}") from exc

    def select(self: NadaTable, *cols: str) -> NadaTable:
        """
        Perform basic select operation on this table, returning a new NadaTable with rows
        consisting of only the specified **cols**

        :param cols: Variadic argument that indicates the names of the columns that will
        be used to construct the output table
        """
        return NadaTable(
            *cols,
            rows=[
                NadaArray(r[i] for i in [self.columns.index(c) for c in cols])
                for r in copy.deepcopy(self._rows)
            ]
        )

    def concat(self: NadaTable, other: NadaTable) -> NadaTable:
        """
        Return a new NadaTable that is the result of concatenating this instance with another

        :param other: NadaTable instance to concatenate with this instance
        """

        if self.columns != other.columns:
            raise ValueError("columns between tables must match to do concat")

        return NadaTable(
            *self.columns,
            rows=copy.deepcopy(self.get_data() + other.get_data())
        )

    def sort_by(self: NadaTable, key_col: str, ascending: bool) -> NadaTable:
        """
        Sort the rows of this table by **key_col** in either ascending or descending order

        :param key_col: Name of the column to key sorting on
        :param ascending: Control ordering on output sort
        """

        new_rows = copy.deepcopy(self._rows)
        functions.odd_even_sort(new_rows, self.get_col_idx(key_col), ascending)

        return NadaTable(*self.columns, rows=new_rows)

    def _aggregate(
            self: NadaTable,
            key_col: str,
            agg_col: str,
            agg_func: Callable[[List[List[secret_int]], int, int], None]
    ) -> NadaTable:
        """
        Perform aggregation function **agg_func** over **agg_col** grouped by **key_col**

        :param key_col: Column to group by
        :param agg_col: Column to sum over
        :param agg_func: aggregation function to perform
        """

        if key_col == agg_col:
            raise ValueError(":key_col: and :agg_col: parameters must be distinct")

        new_rows = [
            NadaArray([
                copy.deepcopy(row[self.get_col_idx(key_col)]),
                copy.deepcopy(row[self.get_col_idx(agg_col)])
            ])
            for row in self.get_data()
        ]
        agg_func(new_rows, 0, 1)

        return NadaTable(key_col, agg_col, rows=new_rows)

    def aggregate_sum(self: NadaTable, key_col: str, agg_col: str) -> NadaTable:
        """
        Sum the contents of **agg_col** grouped by **key_col**

        :param key_col: Column to group by
        :param agg_col: Column to sum over
        """
        return self._aggregate(key_col, agg_col, functions.aggregate_sum)

    def aggregate_max(self: NadaTable, key_col: str, agg_col: str) -> NadaTable:
        """
        Determine the max value of **agg_col** grouped by **key_col**

        :param key_col: Column to group by
        :param agg_col: Column to calculate max over
        """
        return self._aggregate(key_col, agg_col, functions.aggregate_max)

    def aggregate_min(self: NadaTable, key_col: str, agg_col: str):
        """
        Determine the min value of **agg_col** grouped by **key_col**

        :param key_col: Column to group by
        :param agg_col: Column to calculate min over
        """
        return self._aggregate(key_col, agg_col, functions.aggregate_min)


def serialize_input_table(
        arrs: List[List[int]], party: audit.Party, prefix: str
) -> List[NadaArray]:
    """
    Construct and return a NadaTable with inputs that match a certain **prefix** and **party**
    ownership. This is intended be used only for testing with the nada_dsl.audit module.

    :param arrs: Input table
    :param party: Party instance to associate with :arrs:
    :param prefix: String to add as prefix to input data names
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
