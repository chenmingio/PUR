import unittest
from pur_doc import sql, xls_inject, word

from pur_doc.xls_inject import *


TEST_PROJECT = "1111E.001239"
TEST_VENDOR = "48200025"
TEST_PART = "230.033-00"
# TEST_PART_LIST = ['230.033-00', '230.033-10', '230.038-00', '230.038-10']
TEST_PART_LIST = ['230.033-00', '230.033-10']

TEST_PROJECT2 = '1111E.001236' # MEB APS

TEST_DICT = {'parts': {'part_1': {'general_info': {'project': '1111E.001236', 'nr_id': 926, 'part': '191.674-01', 'part_description': 'STECKER GEHAEUSE MONT-GR', 'mtl_group': 'TECH_PLAS', 'raw_mtl': 'PA66 GF40', 'currency': 'CNY', 'risk_level': 'L', 'buyer': 'CHENMI20', 'mgs': 'tbd', 'mgm': 'tbd', 'sqe':
'tbd'}, 'yearly_info': {'volume_year_1': 1330, 'target_price100_year_1': 376.0, 'volume_year_2': 133894, 'target_price100_year_2': 364.72, 'volume_year_3': 294866, 'target_price100_year_3': 353.78, 'volume_year_4': 419310, 'target_price100_year_4': 343.17, 'volume_year_5': 571512, 'target_price100_year_5': 343.17, 'volume_year_6': 66529, 'target_price100_year_6': 343.17, 'volume_year_7': 804498, 'target_price100_year_7': 343.17, 'volume_year_8': 957062, 'target_price100_year_8': 343.17, 'volume_year_9': 658493, 'target_price100_year_9': 343.17}, 'invest_target': {'project_tool_1':
'1111E.001236', 'part_tool_1': '191.674-01', 'tool_tool_1': 1, 'tool_description_tool_1': 'INJECTION AND STANMPING', 'cav_target_tool_1': 4.0, 'cost_target_tool_1': 500000, 'loop_target_tool_1': '3', 'copy_tool_name_tool_1': None, 'copy_tool_cost_tool_1': 0, 'further_invest_name_tool_1': 'ASS. LINE', 'further_invest_cost_tool_1': 260000}, 'quotations': 'TODO'}, 'part_2': {'general_info': {'project': '1111E.001236', 'nr_id': 924, 'part': '229.847-00', 'part_description': 'BEDIENELEMENT', 'mtl_group': 'TECH_PLAS', 'raw_mtl': 'PA66 GF40', 'currency': 'CNY', 'risk_level': 'L', 'buyer': 'CHENMI20', 'mgs': 'tbd', 'mgm': 'tbd', 'sqe': 'tbd'}, 'yearly_info': {'volume_year_1': 1000, 'target_price100_year_1': 510.0, 'volume_year_2': 153000, 'target_price100_year_2': 510.0, 'volume_year_3': 386000, 'target_price100_year_3': 510.0, 'volume_year_4': 511000, 'target_price100_year_4': 510.0, 'volume_year_5': 640000, 'target_price100_year_5': 510.0, 'volume_year_6': 760000, 'target_price100_year_6': 510.0, 'volume_year_7': 920000, 'target_price100_year_7': 510.0, 'volume_year_8': 110000, 'target_price100_year_8': 510.0, 'volume_year_9': 227000, 'target_price100_year_9': 510.0}, 'invest_target': {'project_tool_1': '1111E.001236', 'part_tool_1': '229.847-00', 'tool_tool_1': 1, 'tool_description_tool_1': 'INJECTION TOOL', 'cav_target_tool_1': 2.0, 'cost_target_tool_1': 500000, 'loop_target_tool_1': '3', 'copy_tool_name_tool_1': None, 'copy_tool_cost_tool_1': 0, 'further_invest_name_tool_1': None, 'further_invest_cost_tool_1': 0}, 'quotations': 'TODO'}, 'part_3': {'general_info': {'project': '1111E.001236', 'nr_id': 925, 'part': '234.536-00', 'part_description': 'GEHAEUSE MONT-GR', 'mtl_group': 'TECH_PLAS', 'raw_mtl': 'PA66 GF40', 'currency': 'CNY', 'risk_level': 'L', 'buyer': 'CHENMI20', 'mgs': 'tbd', 'mgm': 'tbd', 'sqe': 'tbd'}, 'yearly_info': {'volume_year_1': 1330, 'target_price100_year_1': 300.0, 'volume_year_2': 133894, 'target_price100_year_2': 300.0, 'volume_year_3': 294866, 'target_price100_year_3': 300.0, 'volume_year_4': 419310, 'target_price100_year_4': 300.0, 'volume_year_5': 571512, 'target_price100_year_5': 300.0, 'volume_year_6': 665299, 'target_price100_year_6': 300.0, 'volume_year_7': 804498, 'target_price100_year_7': 300.0, 'volume_year_8': 957062, 'target_price100_year_8': 300.0, 'volume_year_9': 658493, 'target_price100_year_9': 300.0}, 'invest_target': {'project_tool_1': '1111E.001236', 'part_tool_1': '234.536-00', 'tool_tool_1': 1, 'tool_description_tool_1': 'INJECTION TOOL', 'cav_target_tool_1': 4.0, 'cost_target_tool_1': 500000, 'loop_target_tool_1': '3', 'copy_tool_name_tool_1': None, 'copy_tool_cost_tool_1': 0, 'further_invest_name_tool_1': None, 'further_invest_cost_tool_1': 0}, 'quotations': 'TODO'}}, 'project': {'project': '1111E.001236', 'customer': 'TBD', 'dd_location': 'TBD', 'pjm': 'Jeff Gu', 'pur': 'Chen Ming', 'md': 'Wang Quancheng', 'sqa': 'Daisy Dong', 'me': 'Gu Qi', 'controlling': 'Flynn Tang', 'log': 'Zack Zheng', 'sop_hella_date': '1949-10-01 00:00:00', 'sop_customer_date': '1949-10-01 00:00:00', 'run_rate_date': '1949-10-01 00:00:00', 'pv_hella_date': '1949-10-01 00:00:00', 'year_1_volume': 9999, 'year_2_volume': 9999, 'year_3_volume': 9999, 'year_4_volume': 9999, 'year_5_volume': 9999, 'year_6_volume': 9999, 'year_7_volume': 9999, 'year_8_volume': 9999, 'year_9_volume': 9999, 'year_10_volume': 9999, 'production_line': 'test_production_line', 'fg_part_number': '123456abcd', 'customer_nomination_available': 'YES', 'budget_available': 'YES', 'plant': 1111, 'project_name': 'APS VW MEB'}}


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

        # print(sql.get_part_volume_4project(TEST_PROJECT, TEST_PART))

        # print(sql.assemble_vendors(TEST_PROJECT))

        # print(sql.get_quotation_yearly_info(TEST_PROJECT, TEST_PART, TEST_VENDOR))

        # print(sql.get_quotation_invest_info(TEST_PROJECT, TEST_PART, TEST_VENDOR))

        # print(sql.assemble_quotation_single_part(TEST_PROJECT, TEST_PART))

        # print(sql.get_part_list_by_project_vendor(TEST_PROJECT, TEST_VENDOR))

        # print(sql.assemble_nl_info(TEST_PROJECT, TEST_VENDOR, TEST_PART_LIST))

        pass

    def test_inject(self):

        # xls_inject_risk_eval(TEST_PROJECT2)

        # xls_inject_supplier_selection(TEST_PROJECT2)

        # xls_inject_sb(TEST_PROJECT2)

        pass

    def test_word(self):

        # test_data = sql.assemble_nl_info(TEST_PROJECT, TEST_VENDOR, TEST_PART_LIST)
        # word.generate_nl(test_data)

        pass


if __name__ == '__main__':
    unittest.main()
