import unittest
from pur_doc import sql


TEST_PROJECT = "1111E.001239"
TEST_VENDOR = "48200025"
TEST_PART = "230.033-00"

class TestSum(unittest.TestCase):

    def test_sql_get_part_list_project(self):
        print(sql.get_part_list_project(TEST_PROJECT))
        self.assertEqual(sql.get_part_list_project(TEST_PROJECT), [230.033-00, 230.033-10, 230.038-00, 230.038-10, 178.576-49])


if __name__ == '__main__':
    unittest.main()
