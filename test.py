from pprint import pprint
from pur_doc import sql, xls_inject, word
from pur_doc.xls_inject import *


# test projects
test_project_blank = ""
test_project_none = None
test_project_1 = "1111E.001236"
test_project_fake = "fake_project_id"

# test single parts


# test project/part tuple
test_project_part_tuple_1 = ("1111E.001236", "178.576-15")
test_project_part_tuple_2 = ("1111E.001236", "191.674-01")
test_project_part_tuple_3 = ("1111E.001236", "229.847-00")
test_project_part_tuple_4 = ("1111E.001236", "fake_part_number")

# test project/part tuple
test_project_part_list_tuple_1 = ("1111E.001236", ["178.576-15", "191.674-01", "229.847-00", "234.536-00"])



# test vendors
TEST_VENDOR = "48200025"
TEST_PART = "175.224-40"
TEST_PART_LIST = ['230.033-00', '230.033-10']
TEST_PROJECT_LIST = ['1111E.001377'] #, '1111E.000545', '1111E.000726', '1111E.000903', '1111E.001043', '1111E.001125', '1111E.001236', '1111E.001354', '1111K.000030', '1111K.000167', '1111P.000069', '1111E.000590']
ALL_PROJECT_LIST = sql.get_all_project_list()


# def test_sql(self):


    # self.assertAlmostEqual(sql.get_part_pvo(TEST_PROJECT, TEST_PART), 5073)

    # self.assertEqual(sql.get_part_risk(TEST_PART), 'L')



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

    # pass

# def test_inject(self):

#     xls_inject_risk_eval(TEST_PROJECT2)

#     xls_inject_supplier_selection(TEST_PROJECT2)

#     xls_inject_sb(TEST_PROJECT2)

#     xls_inject_cbd(TEST_PROJECT)

#     pass

# def test_word(self):

#     test_data = sql.assemble_nl_info(TEST_PROJECT, TEST_VENDOR, TEST_PART_LIST)
#     word.generate_nl(test_data)

#     pass

# def test_risk_eval(self):

#     for project in ALL_PROJECT_LIST:
#         part_list = sql.get_project_part_list(project)
#         xls_inject.xls_inject_risk_eval(project, part_list)

# def test_selection_sheet(self):

#     for project in ALL_PROJECT_LIST:
#         xls_inject_supplier_selection(project)


# def test_nl():

#     for project in ALL_PROJECT_LIST:
#         vendor_list = sql.get_vendor_list(project)
#         for vendor in vendor_list:
#             part_list = sql.get_part_list_by_project_vendor(project, vendor)
#             nomi_data = sql.assemble_nl_info(project, vendor, part_list) 
#             print(nomi_data)


# def test_cbd():
#     pass

def test_get_project_info():

    assert sql.get_project_info(test_project_1)['project'] == test_project_1
    print(sql.get_project_info(test_project_1).keys())
    assert sql.get_project_info(test_project_blank) == None
    assert sql.get_project_info(test_project_fake) == None
    assert sql.get_project_info(test_project_none) == None

def test_get_part_list_by_project():
    print(sql.get_part_list_by_project(test_project_1))
    print(sql.get_part_list_by_project(test_project_blank))
    print(sql.get_part_list_by_project(test_project_fake))
    print(sql.get_part_list_by_project(test_project_none))

def test_get_part_general_info():
    print(sql.get_part_general_info(*test_project_part_tuple_1)["part"])

def test_get_part_volume_avg():
    print(">>> volume avg ", sql.get_part_volume_avg(*test_project_part_tuple_1))
    print(">>> volume avg ", sql.get_part_volume_avg(*test_project_part_tuple_2))
    print(">>> volume avg ", sql.get_part_volume_avg(*test_project_part_tuple_3))
    print(">>> volume avg ", sql.get_part_volume_avg(*test_project_part_tuple_4))


def test_get_part_pvo_part():
    print(">>>part_pvo_part ", sql.get_part_pvo_part(*test_project_part_tuple_1))
    print(">>>part_pvo_part ", sql.get_part_pvo_part(*test_project_part_tuple_2))
    print(">>>part_pvo_part ", sql.get_part_pvo_part(*test_project_part_tuple_3))
    print(">>>part_pvo_part ", sql.get_part_pvo_part(*test_project_part_tuple_4))


def test_get_part_lifetime():
    print(">>> part lifetime ", sql.get_part_lifetime(*test_project_part_tuple_1))
    print(">>> part lifetime ", sql.get_part_lifetime(*test_project_part_tuple_2))
    print(">>> part lifetime ", sql.get_part_lifetime(*test_project_part_tuple_3))
    print(">>> part lifetime ", sql.get_part_lifetime(*test_project_part_tuple_4))

def test_get_target_avg_100EUR():
    print(">>> target avg price ", sql.get_part_target_price_avg_100EUR(*test_project_part_tuple_1))
    print(">>> target avg price ", sql.get_part_target_price_avg_100EUR(*test_project_part_tuple_2))
    print(">>> target avg price ", sql.get_part_target_price_avg_100EUR(*test_project_part_tuple_3))
    print(">>> target avg price ", sql.get_part_target_price_avg_100EUR(*test_project_part_tuple_4))

def test_get_part_timing():
    print(">>>part timing ", sql.get_part_timing(*test_project_part_tuple_2).keys())
    print(">>>part timing ", sql.get_part_timing(*test_project_part_tuple_2)['ppap_date'])

# test injection function
def test_xls_inject_risk_eval():
    xls_inject_risk_eval(*test_project_part_list_tuple_1)
