import unittest
from pur_doc import sql, xls_inject

from pur_doc.xls_inject import xls_inject


TEST_PROJECT = "1111E.001239"
TEST_VENDOR = "48200025"
TEST_PART = "230.033-00"

TEST_PROJECT2 = '1111E.001236' # MEB APS

from pur_doc.inject_books import INJECT_BOOK_RISK_EVAL


class TestSum(unittest.TestCase):

    def test_sql(self):

        # self.assertCountEqual(sql.get_project_part_list(TEST_PROJECT), ['230.033-00', '230.033-10', '230.038-00', '230.038-10', '178.576-49'])

        # self.assertAlmostEqual(sql.get_part_pvo(TEST_PROJECT, TEST_PART), 5073)

        # self.assertEqual(sql.get_part_risk(TEST_PART), 'L')

        # self.assertCountEqual(sql.get_project_part_list_4sb(TEST_PROJECT2), [])

        # self.assertCountEqual(sql.get_project_info(TEST_PROJECT), [])
        # print(sql.get_project_info(TEST_PROJECT))

        # print(sql.get_part_general_info(TEST_PART))

        # print(sql.get_part_volume_4project(TEST_PROJECT, TEST_PART))

        # print(sql.get_vendor_info(TEST_VENDOR))

        # print(sql.get_part_year_info(TEST_PROJECT, TEST_PART))

        # print(sql.get_part_invest_target(TEST_PROJECT, TEST_PART))

        # print(sql.assemble_single_part(TEST_PROJECT, TEST_PART))

        # print(sql.assemble_parts_for_project(TEST_PROJECT2))

        # print(sql.assemble_project(TEST_PROJECT2))

        pass

    def test_inject(self):

        xls_inject(INJECT_BOOK_RISK_EVAL, TEST_PROJECT2)

if __name__ == '__main__':
    unittest.main()
