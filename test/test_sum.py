import unittest
from nada_data import basic_ops
from nada_data.nada_array import NadaArray
from nada_dsl import audit
from parameterized import parameterized


class TestSum(unittest.TestCase):

    def run_test(self, party_one_arr: list, party_two_arr: list, expected: int):

        audit.Abstract.initialize(
            {f"p1_input_{i}": party_one_arr[i] for i in range(len(party_one_arr))} |
            {f"p2_input_{i}": party_two_arr[i] for i in range(len(party_two_arr))}
        )

        party_one = audit.Party(name="party_one")
        party_two = audit.Party(name="party_two")

        party_one_input = NadaArray(
            audit.SecretInteger(
                audit.Input(f"p1_input_{i}", party=party_one)
            ) for i in range(len(party_one_arr))
        )
        party_two_input = NadaArray(
            audit.SecretInteger(
                audit.Input(f"p2_input_{i}", party=party_two)
            ) for i in range(len(party_two_arr))
        )

        output = audit.Output(basic_ops.nada_sum(party_one_input + party_two_input), "output", party_one)
        self.assertEqual(output.value.value, expected)

    @parameterized.expand([
        ([1, 2, 3], [2, 3, 4], 15),
        ([5, 6], [7, 10, 5, 2, 9], 44)
    ])
    def test_sum(self, party_one_arr, party_two_arr, expected):
        self.run_test(party_one_arr, party_two_arr, expected)


if __name__ == '__main__':
    unittest.main()
