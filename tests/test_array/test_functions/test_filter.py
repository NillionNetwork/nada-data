import unittest
from typing import List, Callable
from nada_dsl import audit
from parameterized import parameterized
from nada_data.array import functions
from tests.utils import serialize_input_array


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
        self.run_test(first_val, second_val, expected, functions.nada_lt)

    @parameterized.expand([
        (1, 2, 1),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_lteq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, functions.nada_lteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 0)
    ])
    def test_gt(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, functions.nada_gt)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 1)
    ])
    def test_gteq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, functions.nada_gteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_eq(self, first_val: int, second_val: int, expected: int):
        self.run_test(first_val, second_val, expected, functions.nada_eq)


class TestArrayFilter(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 3], functions.nada_lt, 3, [1, 2, 0]),
        ([1, 2, 3], functions.nada_lteq, 3, [1, 2, 3]),
        ([1, 2, 3], functions.nada_gt, 2, [0, 0, 3]),
        ([1, 2, 3], functions.nada_gteq, 2, [0, 2, 3]),
        ([1, 2, 3], functions.nada_eq, 2, [0, 2, 0])
    ])
    def test_filter(
            self, input_arr: List[int], op: Callable, cmp: int, expected: List[int]
    ):

        audit.Abstract.initialize(
            {f"p1_input_{i}": input_arr[i] for i in range(len(input_arr))} |
            {"cmp": cmp}
        )

        input_party = audit.Party(name="input_party")
        cmp_party = audit.Party(name="cmp_party")

        party_one_input = serialize_input_array(input_arr, input_party, "p1_input_")
        output = [
            audit.Output(v, "output", input_party).value.value
            for v in functions.filter_nada_array(
                party_one_input,
                op,
                audit.SecretInteger(audit.Input(name="cmp", party=cmp_party))
            )
        ]
        self.assertEqual(output, expected)

    @parameterized.expand([
        ([1, 2, 3], 3),
        ([3, 2, 1], 3),
        ([4, 1, 3, 2, 5, 6, 5], 6)
    ])
    def test_max(self, input_arr: List[int], expected: int):

        audit.Abstract.initialize(
            {f"p1_input_{i}": input_arr[i] for i in range(len(input_arr))}
        )

        input_party = audit.Party(name="input_party")
        party_one_input = serialize_input_array(input_arr, input_party, "p1_input_")
        output = audit.Output(functions.nada_max(party_one_input), "output", input_party).value.value
        self.assertEqual(output, expected)

    @parameterized.expand([
        ([1, 2, 3], 1),
        ([3, 2, 1], 1),
        ([4, 1, 3, 2, 5, 6, 5], 1)
    ])
    def test_min(self, input_arr: List[int], expected: int):

        audit.Abstract.initialize(
            {f"p1_input_{i}": input_arr[i] for i in range(len(input_arr))}
        )

        input_party = audit.Party(name="input_party")
        party_one_input = serialize_input_array(input_arr, input_party, "p1_input_")
        output = audit.Output(functions.nada_min(party_one_input), "output", input_party).value.value
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()