import unittest
from typing import List
from nada_dsl import audit
from parameterized import parameterized
from nada_data.array import functions
from tests.utils import serialize_input_array


class TestArraySort(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 3], True, [1, 2, 3]),
        ([1, 2, 3], False, [3, 2, 1]),
        ([5, 6, 4, 1, 3, 2], True, [1, 2, 3, 4, 5, 6]),
        ([5, 6, 4, 1, 3, 2], False, [6, 5, 4, 3, 2, 1]),
    ])
    def test_sort(
            self, input_arr: List[int], ascending: bool, expected: List[int]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}": input_arr[i] for i in range(len(input_arr))}
        )

        party = audit.Party(name="party")
        party_one_input = serialize_input_array(input_arr, party, "p1_input_")

        output = [
            audit.Output(v, "output", party).value.value
            for v in functions.sort_nada_array(
                party_one_input,
                ascending=ascending
            )
        ]
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
