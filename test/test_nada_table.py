import unittest
import doctest
from typing import List
from nada_dsl import SecretInteger
from parameterized import parameterized
from nada_data.table import nada_table
from nada_data.array import nada_array


def load_tests(loader, tests, ignore):
    """
    This is a special function that is recognized by unittest and can be used to add
    additional tests to a test suite. In this case, we are adding the doctest tests
    from the table.nada_table module to this test suite.
    """
    tests.addTests(doctest.DocTestSuite(nada_table))
    return tests


class TestNadaTable(unittest.TestCase):

    @parameterized.expand([
        (["a", "b", "c"], ["a", "b"], [[1, 2, 3], [4, 5, 6]], [[1, 2], [4, 5]]),
        (["a", "b", "c"], ["a", "c"], [[1, 2, 3], [4, 5, 6]], [[1, 3], [4, 6]]),
        (["a", "b", "c"], ["b"], [[1, 2, 3], [4, 5, 6]], [[2], [5]]),
        (["a", "b", "c"], ["c"], [[1, 2, 3], [4, 5, 6]], [[3], [6]]),
    ])
    def test_select(self, table_cols: list, select_cols: list, input_rows: List[List], expected_rows: list):

        nt = nada_table.NadaTable(
            *table_cols,
            rows=[nada_array.NadaArray([SecretInteger(v) for v in r]) for r in input_rows]
        )

        output_table = nt.select(*select_cols)
        self.assertEqual(output_table.columns, select_cols)

        for i in range(len(expected_rows)):
            for j in range(len(expected_rows[i])):
                self.assertEqual(expected_rows[i][j], output_table.rows[i][j].inner)


if __name__ == '__main__':
    unittest.main()