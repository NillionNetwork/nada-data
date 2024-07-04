import unittest
from typing import List, Callable
from nada_dsl import audit
from parameterized import parameterized
from nada_data.functions import array


class TestBasicOps(unittest.TestCase):

    def run_test(self, first_val: int, second_val: int, expected: int, cmp_func: callable):

        audit.Abstract.initialize({
            "p1_input": first_val,
            "p2_input": second_val
        })

        party_one = audit.Party(name="party_one")
        party_two = audit.Party(name="party_two")

        party_one_input = audit.SecretInteger(audit.Input(name="p1_input", party=party_one))
        party_two_input = audit.SecretInteger(audit.Input(name="p2_input", party=party_two))

        output = audit.Output(
            cmp_func(party_one_input, party_two_input),
            "output",
            party_one
        )

        self.assertEqual(output.value.value, expected)

    @parameterized.expand([
        (1, 2, 1),
        (2, 1, 0),
        (1, 1, 0)
    ])
    def test_lt(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, array.nada_lt)

    @parameterized.expand([
        (1, 2, 1),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_lteq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, array.nada_lteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 0)
    ])
    def test_gt(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, array.nada_gt)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 1)
    ])
    def test_gteq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, array.nada_gteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_eq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, array.nada_eq)


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
        ([1, 2, 3], [2, 3, 4], array.nada_lt, 3, [1, 2, 0, 2, 0, 0]),
        ([1, 2, 3], [2, 3, 4], array.nada_lteq, 3, [1, 2, 3, 2, 3, 0]),
        ([1, 2, 3], [2, 3, 4], array.nada_gt, 2, [0, 0, 3, 0, 3, 4]),
        ([1, 2, 3], [2, 3, 4], array.nada_gteq, 2, [0, 2, 3, 2, 3, 4]),
        ([1, 2, 3], [2, 3, 4], array.nada_eq, 2, [0, 2, 0, 2, 0, 0])
    ])
    def test_filter(
            self, party_one_arr: List[int], party_two_arr: List[int], op: Callable, cmp: int, expected: List[int]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}": party_one_arr[i] for i in range(len(party_one_arr))} |
            {f"p2_input_{i}": party_two_arr[i] for i in range(len(party_two_arr))} |
            {"cmp": cmp}
        )

        party_one = audit.Party(name="party_one")
        party_two = audit.Party(name="party_two")
        party_three = audit.Party(name="party_three")

        party_one_input, party_two_input = self.serialize_input_arrays(
            party_one_arr, party_two_arr, party_one, party_two
        )

        output = [
            audit.Output(v, "output", party_one).value.value
            for v in array.filter_nada_array(
                party_one_input + party_two_input,
                op,
                audit.SecretInteger(audit.Input(name="cmp", party=party_three))
            )
        ]
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()