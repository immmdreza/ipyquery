import unittest
from src.ipyquery.models.enumerable import Enumerable


class EnumerableTests(unittest.TestCase):
    def test_enum_1(self):
        enum = Enumerable([1, 2, 3, 4])

        l = list(enum)
        print(l)


if __name__ == '__main__':
    unittest.main()
