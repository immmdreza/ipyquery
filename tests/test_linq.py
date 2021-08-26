import unittest
from src.ipyquery import Linq


class Info():
    def __init__(self, name, age, favorites=[]):
        self.name = name
        self.age = age
        self.favorites = favorites


class LinqTests(unittest.TestCase):
    def test_select_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(
            linq.select(lambda x: x * 2).tolist(), [2, 4, 6, 8, 10, 12])

    def test_enum_select_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(
            linq.enum_select(lambda i, x: x * i).tolist(),
            [0, 2, 6, 12, 20, 30])

    def test_enum_select_2(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(linq.enum_select().tolist(), [(0, 1), (1, 2), (2, 3),
                                                       (3, 4), (4, 5), (5, 6)])

    def test_enum_1(self):
        linq = list(enumerate(Linq([1, 2, 3, 4, 5, 6])))
        self.assertEqual(linq, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
                                (5, 6)])

    def test_where_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(linq.where(lambda x: x > 3).tolist(), [4, 5, 6])

    def test_first_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(linq.first(lambda x: x > 3), 4)

    def test_first_2(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertEqual(linq.first(), 1)

    def test_any_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertTrue(linq.any())

    def test_any_2(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertFalse(linq.any(lambda x: x > 6))

    def test_any_3(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        where = linq.where(lambda x: x > 6)
        self.assertFalse(where.any())

    def test_all_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertFalse(linq.all(lambda x: x > 3))

    def test_all_2(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        self.assertTrue(linq.all(lambda x: x < 7))

    def test_order_by_1(self):
        linq = Linq([4, 2, 3, 1, 6, 5])
        self.assertEqual(linq.orderby().tolist(), [1, 2, 3, 4, 5, 6])

    def test_order_by_desc_1(self):
        linq = Linq([4, 2, 3, 1, 6, 5])
        self.assertEqual(linq.orderby_desc().tolist(), [6, 5, 4, 3, 2, 1])

    def test_order_by_2(self):
        linq = Linq([Info("Arash", 24), Info("Sara", 22), Info("Kiarash", 16)])
        query = linq.orderby(lambda x: x.age).select(lambda x: x.name)
        self.assertEqual(query.tolist(), ["Kiarash", "Sara", "Arash"])

    def test_max_1(self):
        linq = Linq([Info("Arash", 24), Info("Sara", 22), Info("Kiarash", 16)])
        max = linq.max(lambda x: x.age)
        self.assertEqual(max.name, "Arash")

    def test_min_1(self):
        linq = Linq([Info("Arash", 24), Info("Sara", 22), Info("Kiarash", 16)])
        min = linq.min(lambda x: x.age)
        self.assertEqual(min.name, "Kiarash")

    def test_sum_1(self):
        linq = Linq([1, 2, 3, 4, 5, 6])
        sum = linq.sum()
        self.assertEqual(sum, 21)

    def test_sum_2(self):
        linq = Linq([Info("Arash", 24), Info("Sara", 22), Info("Kiarash", 16)])
        sum = linq.sum(lambda x: x.age)
        self.assertEqual(sum, 62)

    def test_len_1(self):
        linq = Linq([1, 2, 3])
        self.assertEqual(len(linq), 3)

    def test_avg_1(self):
        linq = Linq([1, 2, 3])
        self.assertEqual(linq.average(), 2.0)

    def test_distinct_1(self):
        linq = Linq([1, 2, 3, 3, 3, 2, 2, 1, 4])
        self.assertEqual(linq.distinct().tolist(), [1, 2, 3, 4])

    def test_distinct_2(self):
        linq = Linq([Info("Arash", 24), Info("Sara", 24), Info("Kiarash", 16)])
        query = linq.distinct(lambda x: x.age).select(lambda x: x.name)
        self.assertEqual(linq.tolist(), ["Arash", "Kiarash"])

    def test_select_many_1(self):
        linq = Linq([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
        query = linq.select_many()
        self.assertEqual(linq.tolist(), [1, 2, 3, 3, 4, 5, 5, 6, 7])

    def test_select_many_2(self):
        linq = Linq([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
        query = linq.select_many().distinct()
        self.assertEqual(linq.tolist(), [1, 2, 3, 4, 5, 6, 7])

    def test_select_many_2(self):
        linq = Linq([[3, 4, 5], [1, 2, 3], [5, 6, 7]])
        query = linq.select_many().distinct().orderby()
        self.assertEqual(linq.tolist(), [1, 2, 3, 4, 5, 6, 7])

    def test_select_many_3(self):
        linq = Linq([
            Info("Arash", 24, ["Programming", "Sports"]),
            Info("Sara", 22, ["Reading", "Sports", "Watching"]),
        ])
        query = linq.select_many(lambda x: x.favorites).distinct()
        self.assertEqual(linq.tolist(),
                         ["Programming", "Sports", "Reading", "Watching"])

    def test_todict_1(self):
        linq = Linq([1, 2, 3, 4])
        self.assertEqual(linq.todict(lambda x: str(x)), {
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
        })

    def test_todict_1(self):
        linq = Linq([1, 2, 3, 4])
        self.assertEqual(
            linq.todict(key_selector=lambda x: str(x),
                        value_selector=lambda y: y**y), {
                            '1': 1,
                            '2': 4,
                            '3': 27,
                            '4': 256,
                        })

    def test_groupby_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.groupby(lambda x: x**0)
        self.assertEqual(query.tolist(), [(1, [1, 2, 3, 4])])

    def test_groupby_2(self):
        linq = Linq([
            Info("Arash", 24, "Programming"),
            Info("Sara", 22, "Programming"),
        ])
        query = linq.groupby(lambda x: x.favorites,
                             value_selector=lambda x: x.name)
        self.assertEqual(query.single(), ('Programming', ['Arash', 'Sara']))

    def test_single_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.groupby(lambda x: x**0)
        self.assertEqual(query.single(), (1, [1, 2, 3, 4]))

    def test_reverse_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.reverse()
        self.assertEqual(query.tolist(), [4, 3, 2, 1])

    def test_remove_all_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.remove_all(lambda x: x > 2)
        self.assertEqual(query.tolist(), [1, 2])

    def test_skip_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.skip(2)
        self.assertEqual(query.tolist(), [3, 4])

    def test_take_1(self):
        linq = Linq([1, 2, 3, 4])
        query = linq.take(2)
        self.assertEqual(query.tolist(), [1, 2])

    def test_example_1(self):
        my_list = Linq([5, 1, 7, 2, 3, 10, 1, 4, 5])

        powered_cleaned = my_list.distinct().where(
            lambda x: x <= 5).orderby().select(lambda x: x**2).tolist()
        self.assertEqual(powered_cleaned, [1, 4, 9, 16, 25])


if __name__ == '__main__':
    unittest.main()
