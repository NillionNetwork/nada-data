import unittest
from typing import List
from nada_dsl import audit
from parameterized import parameterized
from nada_data.functions import odd_even_sort
from tests.utils import serialize_input_table


class TestTableOps(unittest.TestCase):

    @parameterized.expand([
        (
            [[1, 2], [3, 4]],
            True, 0,
            [[1, 2], [3, 4]]
        ),
        (
            [[1, 2], [3, 4]],
            False, 0,
            [[3, 4], [1, 2]]
        ),
        (
            [[7, 8], [1, 6], [9, 2]],
            True, 1,
            [[9, 2], [1, 6], [7, 8]]
        ),
        (
            [[7, 8], [1, 6], [9, 2]],
            False, 1,
            [[7, 8], [1, 6], [9, 2]]
        )
    ])
    def test_sort(
            self,
            input_rows: List[List[int]],
            ascending: bool,
            key_col: int,
            expected: List[int]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}_{j}": val for i, row in enumerate(input_rows) for j, val in enumerate(row)}
        )

        party = audit.Party(name="party")
        data = serialize_input_table(input_rows, party, "p1_input_")
        odd_even_sort(data, key_col, ascending)
        output = [
            [audit.Output(v, "output", party).value.value for v in data[i]]
            for i in range(len(data))
        ]

        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
