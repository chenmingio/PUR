from collections import defaultdict
from pprint import pprint

from app.models.sql_nrm import constant_factory, get_project_data_and_info, get_project_sop_eop, get_vendor_info, \
    get_nl_tool_info, get_nl_invest_info, get_project_vendor_qs_yearly, get_part_general_info, get_part_volume_yearly, \
    get_part_volume_weekly, get_part_price_yearly


def assemble_nl_info(project, vendor, part_list):
    """assemble_nl_info for nomination letter"""

    # project
    # vendor
    # parts [pn1, pn2, pn3]
    # - pnx
    # - - part_volume
    # - general
    # investment
    # < quick reference >
    # vendor_name
    # plant_name

    rc = defaultdict(constant_factory)

    # project general info
    project_dict = get_project_data_and_info(project)
    if project_dict is None:
        project_dict = defaultdict(constant_factory)
    rc['project'] = project_dict

    # sop/eop lifetime attribute
    sop_tuple = get_project_sop_eop(project)
    if sop_tuple is None:
        sop_tuple = defaultdict(constant_factory)

    rc['lifetime'] = sop_tuple
    # TODO true lifetime should get from extra yearly project volume input. Fix later when available.

    # quick reference plant_name
    rc['plant_name'] = project_dict['plant_name']

    # vendor general info
    vendor_dict = get_vendor_info(vendor) or defaultdict(constant_factory)
    rc['vendor'] = vendor_dict
    # quick reference: vendor_name
    rc['vendor_name'] = vendor_dict['duns_name'] # change to duns name!

    # tool
    tools = get_nl_tool_info(project, vendor, part_list)
    rc['tools'] = tools or defaultdict(constant_factory)

    # invest
    invest = get_nl_invest_info(project, vendor, part_list)
    rc['invest'] = invest or defaultdict(constant_factory)

    # project QS info
    rc['qs'] = get_project_vendor_qs_yearly(project, vendor)

    # part info
    # dict['parts'] is a list. The element of this list is
    # a part_dictionary(defaultdict).
    rc['parts'] = []
    for part in part_list:

        part_dict = defaultdict(constant_factory)

        # general part info
        part_general_info = get_part_general_info(project, part)
        if part_general_info is None:
            print(f"[assemble part dict] part_info is None. Use default dict.")
            part_general_info = defaultdict(constant_factory)

        part_dict['general'] = part_general_info
        pprint(f"=======[assemble part dict] part={part_general_info['part']} part_info={part_general_info}")

        # part volume yearly
        part_dict['year_vol'] = get_part_volume_yearly(project, part)

        # part volume weekly
        part_dict['week_vol'] = get_part_volume_weekly(project, part, vendor)

        # part price yearly
        part_dict['part_price100'] = get_part_price_yearly(project, part, vendor)

        # finish the individual part dict and append to part list
        rc['parts'].append(part_dict)

    return rc
