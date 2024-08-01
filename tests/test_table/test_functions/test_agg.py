import unittest
from typing import List, Callable
from nada_dsl import audit
from parameterized import parameterized
from nada_data.table import functions, serialize_input_table
from nada_data.utils import initialize_table_data


class TestTableAgg(unittest.TestCase):

    def run_test(
            self,
            input_rows: List[List[int]],
            key_col: int,
            agg_col: int,
            agg_func: Callable,
            expected: List[List[int]]
    ):

        initialize_table_data("p1_input_", input_rows)
        party = audit.Party(name="party")
        data = serialize_input_table(input_rows, party, "p1_input_")
        agg_func(data, key_col, agg_col)
        output = [
            [audit.Output(v, "output", party).value.value for v in data[i]]
            for i in range(len(data))
        ]

        self.assertEqual(output, expected)

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                0, 1,
                [[1, 0], [1, 5], [3, 0], [3, 7]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                1, 0,
                [[1, 2], [0, 3], [4, 3], [3, 4]]
        ),
    ])
    def test_agg_sum(
            self,
            input_rows: List[List[int]],
            key_col: int,
            agg_col: int,
            expected: List[List[int]]
    ):
        self.run_test(input_rows, key_col, agg_col, functions.aggregate_sum, expected)

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                0, 1,
                [[1, 0], [1, 3], [3, 0], [3, 4]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                1, 0,
                [[1, 2], [0, 3], [3, 3], [3, 4]]
        ),
    ])
    def test_agg_max(
            self,
            input_rows: List[List[int]],
            key_col: int,
            agg_col: int,
            expected: List[List[int]]
    ):
        self.run_test(input_rows, key_col, agg_col, functions.aggregate_max, expected)

    @parameterized.expand([
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                0, 1,
                [[1, 0], [1, 2], [3, 0], [3, 3]]
        ),
        (
                [[1, 2], [3, 4], [1, 3], [3, 3]],
                1, 0,
                [[1, 2], [0, 3], [1, 3], [3, 4]]
        ),
    ])
    def test_agg_min(
            self,
            input_rows: List[List[int]],
            key_col: int,
            agg_col: int,
            expected: List[List[int]]
    ):
        self.run_test(input_rows, key_col, agg_col, functions.aggregate_min, expected)


if __name__ == '__main__':
    unittest.main()
