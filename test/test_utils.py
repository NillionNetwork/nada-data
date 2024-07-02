import unittest
import doctest
from nada_data import utils


def load_tests(loader, tests, ignore):
    """
    This is a special function that is recognized by unittest and can be used to add
    additional tests to a test suite. In this case, we are adding the doctest tests
    from the utils module to this test suite.
    """
    tests.addTests(doctest.DocTestSuite(utils))
    return tests


if __name__ == '__main__':
    unittest.main()
