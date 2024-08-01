import unittest
from typing import List
from nada_dsl import audit
from parameterized import parameterized
from nada_data.array import functions
from nada_data.array import serialize_input_array


class TestArrayArithmetic(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 3], 6),
        ([5, 6], 11)
    ])
    def test_sum(
            self, input_arr: List[int], expected: int
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}": input_arr[i] for i in range(len(input_arr))}
        )

        party = audit.Party(name="party_one")
        output = audit.Output(
            functions.sum_nada_array(
                serialize_input_array(input_arr, party, "p1_input_")
            ),
            "output",
            party
        )
        self.assertEqual(output.value.value, expected)


if __name__ == '__main__':
    unittest.main()
