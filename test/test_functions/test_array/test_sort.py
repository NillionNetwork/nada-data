import unittest
from typing import List
from nada_dsl import audit
from parameterized import parameterized
from nada_data.functions import array


class TestArrayOps(unittest.TestCase):

    @staticmethod
    def serialize_input_arrays(
            party_one_arr: List[int], party_two_arr: List[int], party_one: audit.Party, party_two: audit.Party
    ) -> (array.NadaArray, array.NadaArray):

        party_one_input = array.NadaArray(
            audit.SecretInteger(
                audit.Input(f"p1_input_{i}", party=party_one)
            ) for i in range(len(party_one_arr))
        )
        party_two_input = array.NadaArray(
            audit.SecretInteger(
                audit.Input(f"p2_input_{i}", party=party_two)
            ) for i in range(len(party_two_arr))
        )

        return party_one_input, party_two_input

    @parameterized.expand([
        ([1, 2, 3], [2, 3, 4], True, [1, 2, 2, 3, 3, 4]),
        ([1, 2, 3], [2, 3, 4], False, [4, 3, 3, 2, 2, 1]),
        ([1, 2, 3], [4, 5, 6], True, [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3], [4, 5, 6], False, [6, 5, 4, 3, 2, 1])
    ])
    def test_sort(
            self, party_one_arr: List[int], party_two_arr: List[int], ascending: bool, expected: List[int]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}": party_one_arr[i] for i in range(len(party_one_arr))} |
            {f"p2_input_{i}": party_two_arr[i] for i in range(len(party_two_arr))}
        )

        party_one = audit.Party(name="party_one")
        party_two = audit.Party(name="party_two")

        party_one_input, party_two_input = self.serialize_input_arrays(
            party_one_arr, party_two_arr, party_one, party_two
        )

        output = [
            audit.Output(v, "output", party_one).value.value
            for v in array.sort_nada_array(
                party_one_input + party_two_input,
                ascending=ascending
            )
        ]
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
