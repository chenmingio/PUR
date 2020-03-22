from datetime import date
from pprint import pprint

from app.models.logisitcs import Part
from app.models.sql_logistics import build_volumes_object_for_nrm_vendor, get_vendor_list_from_weekly_demand, \
    get_nl_part_volume_by_vendor_and_year, get_fiscal_year, get_apn_part_volume_by_vendor_and_year


def test_part_get_project_dict_from_nrm():
    part_1 = Part("324.526-00", 1111)
    print(">>>vendor dict: ", part_1.get_vendor_dict_from_nrm("1111E..001275", "48201703"))
    print(">>>project dict: ", part_1.get_project_dict_list_from_nrm())


def test_build_volumes_object_for_nrm_vendor():
    print(build_volumes_object_for_nrm_vendor("1000E.003040", "232.943-00", "80013527"))


def test_get_delivery():
    part_1 = Part("325.607-00", 1111)
    print(part_1.get_delivery(48200042))
    part_2 = Part("325.608-00", 1111)
    print(part_2.get_delivery(48200042))
    part_3 = Part("325.609-04", 1111)
    print(part_3.get_delivery(48200087))


def test_get_vendor_list_from_weekly_demand():
    print(get_vendor_list_from_weekly_demand('170.467-30'))
    print(get_vendor_list_from_weekly_demand('324.526-00'))
    print(get_vendor_list_from_weekly_demand('177.306-36'))


def test_get_nl_part_volume_by_vendor_and_year():
    print(get_nl_part_volume_by_vendor_and_year("325.607-00", 48200042, 2020))
    print(get_nl_part_volume_by_vendor_and_year("325.607-00", 48200042, 2019))


def test_get_apn_part_volume_by_vendor_and_year():
    print(get_apn_part_volume_by_vendor_and_year("325.607-00", 48200042, 2020))
    print(get_apn_part_volume_by_vendor_and_year("325.607-00", 48200042, 2019))

def test_get_fiscal_year():
    assert get_fiscal_year(date(2019, 3, 1)) == 2018
    assert get_fiscal_year(date(2019, 6, 1)) == 2019
