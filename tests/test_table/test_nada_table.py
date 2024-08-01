import unittest
import doctest
from typing import List, Callable, Dict
from nada_dsl import audit
from parameterized import parameterized
from nada_data.table import nada_table, NadaTable, serialize_input_table
from nada_data.utils import initialize_table_data, initialize_table_data_multi


def load_tests(loader, tests, ignore):
    """
    This is a special function that is recognized by unittest and can be used to add
    additional tests to a test suite. In this case, we are adding the doctest tests
    from the utils module to this test suite.
    """
    tests.addTests(doctest.DocTestSuite(nada_table))
    return tests


class TestNadaTable(unittest.TestCase):

    @parameterized.expand([
        (
                ["a", "b", "c"],
                [[1, 2, 3], [4, 5, 6]],
                "NadaTable | cols=['a','b','c'] | rows=2 | parties=['party']"
        )
    ])
    def test_create_single_party(self, cols: list, input_rows: List[List[int]], expected_str: str):

        initialize_table_data("p1_input_", input_rows)
        party = audit.Party(name="party")
        nt = NadaTable(
            *cols,
            rows=serialize_input_table(input_rows, party, "p1_input_")
        )
        self.assertEqual(expected_str, str(nt))

    @parameterized.expand([
        (
                ["d", "e", "f"],
                {"party_one": [[1, 2, 3], [3, 2, 1]], "party_two": [[4, 5, 6]]},
                "NadaTable | cols=['d','e','f'] | rows=3 | parties=['party_one','party_two']"
        )
    ])
    def test_create_multi_party(self, cols: list, inputs: Dict[str, List[List[int]]], expected_str: str):

        initialize_table_data_multi(inputs)
        tables = [
            serialize_input_table(
                inputs[party_name], audit.Party(name=party_name), prefix=f"{party_name}_"
            ) for party_name in inputs.keys()
        ]
        nt = NadaTable(
            *cols,
            rows=[row for table in tables for row in table]
        )
        self.assertEqual(expected_str, str(nt))

    @parameterized.expand([
        (
            ["a", "b", "c"], ["a", "b"],
            [[1, 2, 3], [4, 5, 6]], [[1, 2], [4, 5]]
        ),
        (
            ["a", "b", "c"], ["a", "c"],
            [[1, 2, 3], [4, 5, 6]], [[1, 3], [4, 6]]
        ),
        (
            ["a", "b", "c"], ["b"],
            [[1, 2, 3], [4, 5, 6]], [[2], [5]]
        ),
        (
            ["a", "b", "c"], ["c"],
            [[1, 2, 3], [4, 5, 6]], [[3], [6]]
        ),
    ])
    def test_select(
            self, cols: list, select_cols: list, input_rows: List[List[int]], expected_rows: List[List[int]]
    ):

        initialize_table_data("p1_input_", input_rows)
        party = audit.Party(name="party")
        nt = NadaTable(
            *cols,
            rows=serialize_input_table(input_rows, party, "p1_input_")
        )

        output_table = nt.select(*select_cols)
        self.assertEqual(output_table.columns, select_cols)

        output = [
            [audit.Output(v, "output", party).value.value for v in output_table._rows[i]]
            for i in range(len(nt._rows))
        ]
        self.assertEqual(output, expected_rows)

    @parameterized.expand([
        (
            ["a", "b"], "a", True,
            [[1, 2], [3, 4]],
            [[1, 2], [3, 4]]
        ),
        (
            ["a", "b"], "a", False,
            [[1, 2], [3, 4]],
            [[3, 4], [1, 2]]
        ),
        (
            ["a", "b", "c"], "b", True,
            [[7, 8, 2], [1, 6, 5], [9, 2, 3]],
            [[9, 2, 3], [1, 6, 5], [7, 8, 2]]
        ),
        (
            ["a", "b", "c"], "b", False,
            [[7, 8, 2], [1, 6, 5], [9, 2, 3]],
            [[7, 8, 2], [1, 6, 5], [9, 2, 3]]
        )
    ])
    def test_sort_by(
            self, cols: list, key_col: str, ascending: bool, input_rows: List[List[int]], expected: List[List[int]]
    ):

        initialize_table_data("p1_input_", input_rows)
        party = audit.Party(name="party")
        nt = NadaTable(
            *cols,
            rows=serialize_input_table(input_rows, party, "p1_input_")
        )
        nt.sort_by(key_col, ascending)

        output = [
            [audit.Output(v, "output", party).value.value for v in nt._rows[i]]
            for i in range(len(nt._rows))
        ]

        self.assertEqual(output, expected)

    def run_agg_test(
            self,
            input_rows: List[List[int]],
            cols: List[str],
            key_col: str,
            agg_col: str,
            agg_func: Callable,
            expected: List[List[int]]
    ):

        initialize_table_data("p1_input_", input_rows)
        party = audit.Party(name="party")
        nt = NadaTable(
            *cols,
            rows=serialize_input_table(input_rows, party, "p1_input_")
        )
        agg_func(nt, key_col, agg_col)

        output = [
            [audit.Output(v, "output", party).value.value for v in nt._rows[i]]
            for i in range(len(nt._rows))
        ]

        self.assertEqual(output, expected)

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "a", "b",
                [[1, 0], [1, 5], [3, 0], [3, 7]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "b", "a",
                [[1, 2], [0, 3], [4, 3], [3, 4]]
        ),
    ])
    def test_aggregate_sum(
            self,
            input_rows: List[List[int]],
            cols: List[str],
            key_col: str,
            agg_col: str,
            expected: List[List[int]]
    ):
        self.run_agg_test(
            input_rows, cols, key_col, agg_col, nada_table.NadaTable.aggregate_sum, expected
        )

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "a", "b",
                [[1, 0], [1, 3], [3, 0], [3, 4]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "b", "a",
                [[1, 2], [0, 3], [3, 3], [3, 4]]
        ),
    ])
    def test_aggregate_max(
            self,
            input_rows: List[List[int]],
            cols: List[str],
            key_col: str,
            agg_col: str,
            expected: List[List[int]]
    ):
        self.run_agg_test(
            input_rows, cols, key_col, agg_col, nada_table.NadaTable.aggregate_max, expected
        )

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "a", "b",
                [[1, 0], [1, 2], [3, 0], [3, 3]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                ["a", "b"], "b", "a",
                [[1, 2], [0, 3], [1, 3], [3, 4]]
        ),
    ])
    def test_aggregate_min(
            self,
            input_rows: List[List[int]],
            cols: List[str],
            key_col: str,
            agg_col: str,
            expected: List[List[int]]
    ):
        self.run_agg_test(
            input_rows, cols, key_col, agg_col, nada_table.NadaTable.aggregate_min, expected
        )


if __name__ == '__main__':
    unittest.main()
