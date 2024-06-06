from __future__ import annotations
from typing import List, Callable
from nada_dsl import SecretInteger
from nada_data.nada_array import NadaArray


class NadaTable:
    def __init__(
            self: NadaTable,
            *columns: str,
            data: List[NadaArray] = None
    ):

        self.columns = [c for c in columns]
        self.data = self._set_data(data)

    def __str__(self: NadaTable):
        return f"NadaTable({', '.join([c for c in self.columns])})"

    def __repr__(self: NadaTable):
        return str(self)

    def set_columns(self: NadaTable, columns: List[str]):

        self.columns = []
        for c in columns:
            if not isinstance(c, str):
                raise TypeError("column names must be str")
            if c in self.columns:
                raise ValueError(f"table already contains a column with name '{c}'")
            self.columns.append(c)

        return self

    def _set_data(self: NadaTable, data: List[NadaArray]):

        output = []
        for d in data:
            if not isinstance(d, NadaArray):
                raise TypeError("rows must be NadaArray instances")
            if len(d) != len(self.columns):
                raise ValueError("rows must contain the same number of elements as column list")
            output.append(d)
        return output

    def set_data(self: NadaTable, data: List[NadaArray]):
        self.data = self._set_data(data)
        return self

    def get_col_idx(self: NadaTable, col_name: str):
        try:
            return self.columns.index(col_name)
        except ValueError:
            raise ValueError(f"column {col_name} not in {self}")

    def add_row(self: NadaTable, row: NadaArray):
        if len(self.columns) != len(row):
            raise ValueError("input row length must match length of table columns")
        self.data.append(row)

    def select(
            self: NadaTable,
            *args: str
    ):
        return NadaTable(
            *args,
            data=[
                NadaArray(r[i] for i in [self.columns.index(c) for c in args])
                for r in self.data
            ]
        )

    def aggregate(
            self: NadaTable,
            key_col: str,
            agg_col: str,
            agg_func: Callable[[List[SecretInteger]], NadaTable]
    ):

        agg_data = {}
        for r in self.data:

            k = r[self.columns.index(key_col)]
            v = r[self.columns.index(agg_col)]
            if k in agg_data:
                agg_data[k].append(v)
            else:
                agg_data[k] = NadaArray(v)

        output_table = NadaTable(key_col, agg_col)
        for k, v in agg_data.items():
            output_table.add_row(NadaArray(k, agg_func(v)))

        return output_table

    def join(
            self: NadaTable,
            other: NadaTable,
            key_col: str
    ):

        k_idx_self = self.columns.index(key_col)
        k_idx_other = other.columns.index(key_col)