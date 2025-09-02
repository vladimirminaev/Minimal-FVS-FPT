from minimal_fvs_fpt.utils import get_list_of_proper_subsets
import unittest


class TestUtils(unittest.TestCase):
    def test_get_list_of_proper_subsets(self):
        test_case = range(0, 4)
        self.assertEqual(
            len(get_list_of_proper_subsets(test_case)), pow(2, len(test_case)) - 1
        )
