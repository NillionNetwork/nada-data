import unittest
from nada_data import basic_ops
from nada_dsl import audit
from parameterized import parameterized


def set_up_parties():
    """
    Basic two party setup. Can't do this in unittest built in setUp() function because it
    needs to run after the abstract.Initialize function.
    """

    party_one = audit.Party(name="party_one")
    party_two = audit.Party(name="party_two")

    party_one_input = audit.SecretInteger(audit.Input(name="p1_input", party=party_one))
    party_two_input = audit.SecretInteger(audit.Input(name="p2_input", party=party_two))

    return party_one, party_one_input, party_two_input


def get_output(cmp: audit.SecretInteger, output_party: audit.Party):
    return audit.Output(cmp, "output", output_party)


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

        output = get_output(
            cmp_func(party_one_input, party_two_input),
            party_one
        )

        self.assertEqual(output.value.value, expected)

    @parameterized.expand([
        (1, 2, 1),
        (2, 1, 0),
        (1, 1, 0)
    ])
    def test_lt(self, first_val, second_val, expected):
        self.run_test(first_val, second_val, expected, basic_ops.nada_lt)

    @parameterized.expand([
        (1, 2, 1),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_lteq(self, first_val, second_val, expected):
        self.run_test(first_val, second_val, expected, basic_ops.nada_lteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 0)
    ])
    def test_gt(self, first_val, second_val, expected):
        self.run_test(first_val, second_val, expected, basic_ops.nada_gt)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 2),
        (1, 1, 1)
    ])
    def test_gteq(self, first_val, second_val, expected):
        self.run_test(first_val, second_val, expected, basic_ops.nada_gteq)

    @parameterized.expand([
        (1, 2, 0),
        (2, 1, 0),
        (1, 1, 1)
    ])
    def test_eq(self, first_val, second_val, expected):
        self.run_test(first_val, second_val, expected, basic_ops.nada_eq)


if __name__ == '__main__':
    unittest.main()
