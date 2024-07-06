import unittest
from typing import List, Callable
from nada_dsl import audit, SecretInteger
from parameterized import parameterized
from nada_data.functions import aggregate_sum, aggregate_max, aggregate_min
from tests.utils import serialize_input_table


class TestTableAgg(unittest.TestCase):

    def run_test(
            self,
            input_rows: List[List[int]],
            key_col: int,
            agg_col: int,
            agg_func: Callable,
            expected: List[List[int]]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}_{j}": val for i, row in enumerate(input_rows) for j, val in enumerate(row)}
        )

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
        self.run_test(input_rows, key_col, agg_col, aggregate_sum, expected)

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
        self.run_test(input_rows, key_col, agg_col, aggregate_max, expected)

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
        self.run_test(input_rows, key_col, agg_col, aggregate_min, expected)


if __name__ == '__main__':
    unittest.main()
