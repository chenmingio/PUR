import unittest
from pur_doc import sql, xls_inject, word

from pur_doc.xls_inject import *


TEST_PROJECT = "1111E.001236"
TEST_VENDOR = "48200025"
TEST_PART = "175.224-40"
TEST_PART_LIST = ['230.033-00', '230.033-10']
TEST_PROJECT_LIST = ['1111E.001377'] #, '1111E.000545', '1111E.000726', '1111E.000903', '1111E.001043', '1111E.001125', '1111E.001236', '1111E.001354', '1111K.000030', '1111K.000167', '1111P.000069', '1111E.000590']
ALL_PROJECT_LIST = sql.get_all_project_list()


class TestSum(unittest.TestCase):

    def test_sql(self):


        # self.assertAlmostEqual(sql.get_part_pvo(TEST_PROJECT, TEST_PART), 5073)

        # self.assertEqual(sql.get_part_risk(TEST_PART), 'L')

        # print(sql.get_project_part_list(TEST_PROJECT3))

        # self.assertCountEqual(sql.get_project_info(TEST_PROJECT), [])

        # print(sql.get_project_info(TEST_PROJECT))

        # print(sql.get_part_general_info(TEST_PART))

        # print(sql.get_part_volume(TEST_PROJECT, TEST_PART))

        # print(sql.get_vendor_info('48200042'))

        # print(sql.get_part_year_info(TEST_PROJECT, TEST_PART))

        # print(sql.get_part_invest_target(TEST_PROJECT, TEST_PART))

        # print(sql.assemble_single_part(TEST_PROJECT, TEST_PART))

        # print(sql.assemble_parts_for_project('1111E.001377', ['221.428-50']))

        # print(sql.get_part_quotation_pvo(TEST_PROJECT, TEST_PART, TEST_VENDOR))

        # print(sql.get_part_quotation_qs(TEST_PROJECT, TEST_PART, TEST_VENDOR))


        # print(sql.assemble_vendors(TEST_PROJECT))

        # print(sql.get_quotation_yearly_info(TEST_PROJECT, TEST_PART, TEST_VENDOR))

        # print(sql.get_quotation_invest_info(TEST_PROJECT, TEST_PART, TEST_VENDOR))

        # print(sql.assemble_quotation_single_part(TEST_PROJECT, TEST_PART))

        # print(sql.get_part_list_by_project_vendor(TEST_PROJECT, TEST_VENDOR))

        # print(sql.assemble_nl_info(TEST_PROJECT, TEST_VENDOR, TEST_PART_LIST))

        # loop over project lists for batch unit test

        # test a individual part under it's project
        # inject_data = sql.assemble_project('1111P.000088', ['173.889-01'])
        # print(inject_data)

        # for project in TEST_PROJECT_LIST:
        #     part_list = sql.get_project_part_list(project)
        #     # print(part_list)
        #     inject_data = sql.assemble_project(project, part_list)
        #     print(inject_data)

            # vendor_list = sql.get_vendor_list(project)
            # for vendor in vendor_list:
            #     part_list = sql.get_part_list_by_project_vendor(project, vendor) 
            #     # inject_data = sql.assemble_nl_info(project, vendor, part_list)
            #     # print(inject_data)
            #     for part in part_list:
            #         print(sql.get_part_volume_inweek(project, part, vendor))

        # print(sql.get_all_project_list())

        pass

    def test_inject(self):

        # xls_inject_risk_eval(TEST_PROJECT2)

        # xls_inject_supplier_selection(TEST_PROJECT2)

        # xls_inject_sb(TEST_PROJECT2)

        # xls_inject_cbd(TEST_PROJECT)

        pass

    def test_word(self):

        # test_data = sql.assemble_nl_info(TEST_PROJECT, TEST_VENDOR, TEST_PART_LIST)
        # word.generate_nl(test_data)

        pass

    def test_risk_eval(self):

        # for project in ALL_PROJECT_LIST:
        #     part_list = sql.get_project_part_list(project)
        #     xls_inject.xls_inject_risk_eval(project, part_list)

        pass

    def test_selection_sheet(self):

        # for project in ALL_PROJECT_LIST:
        #     xls_inject_supplier_selection(project)

        pass

    def test_nl(self):
        pass

    def test_cbd(self):
        pass

if __name__ == '__main__':
    unittest.main()
