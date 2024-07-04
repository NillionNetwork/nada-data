import unittest
from nada_data import nada_array
import doctest


def load_tests(loader, tests, ignore):
    """
    This is a special function that is recognized by unittest and can be used to add
    additional tests to a test suite. In this case, we are adding the doctest tests
    from the array.nada_array module to this test suite.
    """
    tests.addTests(doctest.DocTestSuite(nada_array))
    return tests


if __name__ == '__main__':
    unittest.main()
