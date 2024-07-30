import unittest
from nada_dsl import audit
from parameterized import parameterized
from typing import List, Dict
from tests.utils import serialize_input_array, initialize_array_data
from nada_data.array.nada_array import NadaArray


class TestNadaArray(unittest.TestCase):

    @parameterized.expand([
        (
                [1, 2, 3],
                "NadaArray | len=3 | parties=['party']"
        ),
        (
                [6, 5, 4, 3, 2, 1],
                "NadaArray | len=6 | parties=['party']"
        )
    ])
    def test_create_single_party(
            self, input_values: List[int], expected_str: str
    ):

        initialize_array_data("p1_input_", input_values)
        party = audit.Party(name="party")
        arr = serialize_input_array(input_values, party, "p1_input_")
        self.assertEqual(expected_str, str(arr))

    @parameterized.expand([
        (
                {"party_one": [1, 2, 3], "party_two": [4, 5, 6]},
                "NadaArray | len=6 | parties=['party_one', 'party_two']"
        ),
        (
                {"partyOne": [8, 6, 4, 2], "partyTwo": [1, 3, 5, 7], "partyThree": [9, 10]},
                "NadaArray | len=10 | parties=['partyOne', 'partyThree', 'partyTwo']"
        )
    ])
    def test_create_multi_party(self, inputs: Dict[str, List[int]], expected_str: str):

        audit.Abstract.initialize({
            f"{party_name}_{i}": inputs[party_name][i]
            for party_name in inputs.keys()
            for i in range(len(inputs[party_name]))
        })

        arrs = [
            serialize_input_array(
                inputs[party_name], audit.Party(name=party_name), prefix=f"{party_name}_"
            ) for party_name in inputs.keys()
        ]
        self.assertEqual(expected_str, str(sum(arrs, NadaArray())))


if __name__ == '__main__':
    unittest.main()
