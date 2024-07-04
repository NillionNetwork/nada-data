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
        ([1, 2, 3], [2, 3, 4], 15),
        ([5, 6], [7, 10, 5, 2, 9], 44)
    ])
    def test_sum(
            self, party_one_arr: List[int], party_two_arr: List[int], expected: int
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

        output = audit.Output(
            array.sum_nada_array(party_one_input + party_two_input), "output", party_one
        )
        self.assertEqual(output.value.value, expected)


if __name__ == '__main__':
    unittest.main()