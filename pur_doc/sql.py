'''build dict by sql query and factory'''
import sqlite3
from collections import defaultdict

from pur_doc.constant import DB_URL, EX_RATE, LOCAL_SB_THRESHOLD

CONN = sqlite3.connect(DB_URL, check_same_thread=False)
CONN_f = sqlite3.connect(DB_URL, check_same_thread=False)

# CONN_f.row_factory = dict_factory
CONN_f.row_factory = sqlite3.Row

# Remind word for missing info
REMIND_WORD = 'None'

DEFAULT_WPY = 50


def constant_factory():
    '''used for defaultdict return'''
    return REMIND_WORD


def assemble_nl_info(project, vendor, part_list):
    '''assemble_nl_info for normination letter'''

    # project
    # vendor
    # parts [pn1, pn2, pn3]
    # - pnx
    # - - part_volume
    # - general
    # < quick reference >
    # vendor_name
    # plant_name

    rc = defaultdict(constant_factory)

    # project general info
    project_dict = get_project_info(project)
    if project_dict is None:
        project_dict = defaultdict(constant_factory)

    # sop/eop
    sop_tuple = get_project_sop_eop(project)
    if sop_tuple is None:
        sop_tuple = defaultdict(constant_factory)

    rc['lifetime'] = sop_tuple

    # quick reference in Jinja
    rc['plant_name'] = project_dict['plant_name']
    rc['project'] = project_dict

    # vendor general info
    vendor_dict = get_vendor_info(vendor)
    if vendor_dict is None:
        vendor_dict = defaultdict(constant_factory)
    # quick reference in Jinja
    rc['vendor_name'] = vendor_dict['vendor_name']
    rc['vendor'] = vendor_dict

    # part info
    # dict['parts'] is a list. The element of this list is
    # a part_dictionary(defaultdict).
    rc['parts'] = []
    for part in part_list:

        part_dict = defaultdict(constant_factory)

        # general part info
        part_info = get_part_general_info(project, part)
        if part_info is None:
            part_info = defaultdict(constant_factory)

        part_dict['general'] = part_info

        # part volume yearly
        part_dict['year_vol'] = get_part_volume_yearly(project, part)

        # part volume weekly
        part_dict['week_vol'] = get_part_volume_weekly(project, part, vendor)

        # finish the individual part dict and append to part list
        rc['parts'].append(part_dict)

    return rc


def get_project_sop_eop(project):
    """find the min/max year number in rfq_part year column where the quantity
    is not 0 as real SOP/EOP year"""

    cursor = CONN_f.cursor()
    context = (project, )

    cursor.execute(
        '''SELECT MIN(year) AS sop, MAX(year) AS EOP FROM rfq_part
              WHERE project=? AND volume > 0''', context)

    return cursor.fetchone()


def get_vendor_weeks_per_year(vendor):

    cursor = CONN_f.cursor()
    context = (vendor, )

    # get week per year of vendor
    cursor.execute(
        '''SELECT weeks_per_year AS wpy FROM vendor_production AS VP
              WHERE VP.vendor=?''', context)

    row = cursor.fetchone()
    if row:
        return row['wpy']


def get_part_volume_weekly(project, part, vendor):
    '''get part volume devided by weeks_per_year of vendor and mulitiply 1.3'''

    wpy = get_vendor_weeks_per_year(vendor)

    if wpy is None or wpy.isdigit() is False:
        wpy = DEFAULT_WPY

    temp_dict = get_part_volume_yearly(project, part)
    for vol in temp_dict:
        vol = vol / wpy

    return temp_dict


def get_part_volume_yearly(project, part):
    '''get part volume '''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT RP.year AS year, RP.volume AS vol FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    part_vol_dict = defaultdict(constant_factory)

    if rows:
        for row in rows:
            year = row['year']
            vol = row['vol']
            part_vol_dict[year] = vol

    return part_vol_dict


def get_part_volume_sum(project, part):
    '''get part volume'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT SUM(volume) AS vol_sum FROM rfq_part
              WHERE project=? AND part=?''', context)

    row = cursor.fetchone()
    if row:
        return row['vol_sum']


def get_part_target_price_avg_100EUR(project, part):
    pvo_part = get_part_target_pvo_part(project, part)
    lifetime = get_part_lifetime(project, part)
    vol_sum = get_part_volume_sum(project, part)

    if pvo_part and lifetime and vol_sum:
        target_price = pvo_part / lifetime / vol_sum / EX_RATE['EUR'] * 100
        return target_price


def get_part_target_price(project, part):
    '''get part target price'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT DISTINCT RP.target_price100 FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return (result)


def get_part_invest_target(project, part):
    ''''''
    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT DISTINCT *
              FROM rfq_invest AS RI
              WHERE RI.project=? AND RI.part=? ORDER BY RI.tool''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'tool')

    return (result)


def get_part_general_info(project, part):
    '''return a dictionary with titles and values about part general info
    (
eg. part_description/mtl_group/etc,
) based on single part number (
project info also involved for nr_id cross location,
)'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT DISTINCT * FROM part_data AS pd
        LEFT JOIN mgm USING(mtl_group)
        LEFT JOIN mgs_sqe USING(mtl_group)
        LEFT JOIN plant USING(plant)
        WHERE pd.project=? AND pd.part=?''', context)

    return cursor.fetchone()


def search_invest_info(project, vendor, part):
    '''fine invest info based on given pn'''
    cursor = CONN.cursor()
    context = (project, vendor, part)

    cursor.execute(
        '''SELECT * FROM nomi_invest AS NI WHERE NI.project=? AND
    NI.vendor=? AND NI.part=? ORDER BY NI.tool''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'invest')

    return result


def get_vendor_list(project):
    '''prepare a list of vendors,
 whick later quotation of each part can refer to '''

    cursor = CONN.cursor()
    context = (project, )

    cursor.execute(
        '''SELECT DISTINCT vendor FROM sourcing_concept WHERE project=? ORDER
        BY vendor''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result


def get_nominated_vendor(project, part):
    '''check the sourcing_concept which supplier is marked as nominated'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT DISTINCT vendor FROM sourcing_concept WHERE project=?
        AND part=? AND vendor_nominated='X' ORDER BY vendor''', context)

    row = cursor.fetchone()

    result = row[0] if row else None

    return result


def get_vendor_info(vendor):
    '''get all general vendor info'''

    cursor = CONN_f.cursor()
    context = (vendor, )

    cursor.execute(
        '''SELECT * FROM
    vendor_contact AS VC
    LEFT JOIN vendor_basic AS VB ON VC.vendor=VB.vendor
    LEFT JOIN contract AS C ON VC.vendor=C.vendor
    LEFT JOIN quality AS Q ON VC.vendor=Q.vendor
    LEFT JOIN vendor_production AS P on VC.vendor=P.vendor
    WHERE VC.vendor=?''', context)

    row = cursor.fetchone()

    if row:
        return row
    else:
        return None


def get_project_info(project):
    '''from TABLE: project_data + project_info'''
    cursor = CONN_f.cursor()
    context = (project, )
    cursor.execute(
        '''SELECT * FROM project_data LEFT JOIN project_info USING (project)
            LEFT JOIN plant USING (plant) WHERE project=?''', context)
    row = cursor.fetchone()
    return row


def get_project_part_list(project):
    '''given a project,
 return a list with all parts by search the part_data sheet'''

    cursor = CONN.cursor()
    context = (project, )

    cursor.execute(
        '''SELECT DISTINCT part FROM part_data WHERE project=?
        ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result

    # def get_part_quotation_qs(project, part, vendor):
    '''get total quick saving for a quotation'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute(
        '''SELECT SUM(
qs,
) FROM nomi_part WHERE project=? AND part=? AND vendor=?''', context)

    row = cursor.fetchone()
    result = row[0] or 0

    return result


def get_part_quotation_pvo(project, part, vendor):
    '''return PVO by project and part and vendor'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    # get price pvo
    cursor.execute(
        '''SELECT SUM(
year_PVO,
) FROM (
SELECT project,
 part,
 year,
 volume*price100/100 AS year_PVO FROM rfq_part NATURAL JOIN nomi_part
        WHERE project=? AND part=? AND vendor=?,
)''', context)

    row = cursor.fetchone()

    part_pvo = row[0] if row[0] else 0

    cursor.execute(
        '''SELECT SUM(invest_cost,) FROM
        (SELECT tool_cost+further_invest_cost AS invest_cost FROM nomi_invest
        WHERE project=? AND part=? AND vendor=?,
)''', context)

    row = cursor.fetchone()

    invest_pvo = row[0] if row[0] else 0

    # pvo = (part_pvo + invest_pvo) / EX_RATE['EUR']
    pvo = part_pvo + invest_pvo

    return int(pvo)


def get_part_target_pvo_part(project, part):
    '''PVO target only for parts'''
    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT SUM(year_PVO) AS target_pvo_part FROM
        (SELECT volume*target_price100/100 AS year_PVO FROM rfq_part
        WHERE project=? AND part=?)''', context)

    row = cursor.fetchone()
    if row:
        return row['target_pvo_part']
    else:
        return None


def get_part_target_pvo_investment(project, part):
    '''PVO target only for investment'''
    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT SUM(invest_target) AS invest_target_pvo
        FROM (
            SELECT cost_target+further_invest_cost AS invest_target
                FROM rfq_invest
            WHERE project=? AND part=?)''', context)

    row = cursor.fetchone()
    if row:
        return row['invest_target_pvo']
    else:
        return None


def get_part_target_pvo_total(project, part):
    '''add target pvo of part and investment together'''
    target_pvo_part = get_part_target_pvo_part(project, part)
    target_pvo_investment = get_part_target_pvo_investment(project, part)

    if target_pvo_investment and target_pvo_part:
        return (target_pvo_investment + target_pvo_part)
    elif target_pvo_part:
        return target_pvo_part
    elif target_pvo_investment:
        return target_pvo_investment
    else:
        return None


def get_part_lifetime(project, part):
    '''real lifetime according to row with volume from TABLE rfq_part'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT COUNT(*) AS count
        FROM rfq_part WHERE project=? AND part=?''', context)
    row = cursor.fetchone()
    if row:
        return row['count']


def get_part_pvo(project, part):
    '''return PVO by project and part'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT SUM(
year_PVO,
) FROM (
SELECT volume*target_price100/100 AS year_PVO FROM rfq_part
        WHERE project=? AND part=?,)''', context)

    row = cursor.fetchone()
    part_pvo = row[0] if row[0] else 0

    cursor.execute(
        '''SELECT SUM(
invest_target,
) FROM (
SELECT cost_target+further_invest_cost AS invest_target FROM rfq_invest
        WHERE project=? AND part=?,)''', context)

    row = cursor.fetchone()

    invest_pvo = row[0] if row[0] else 0

    # pvo = (part_pvo + invest_pvo) / EX_RATE['EUR']
    pvo = part_pvo + invest_pvo

    return int(pvo)


def get_part_risk(project, part):
    '''get risk level'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT risk_level FROM part_data WHERE project=? AND part=?''',
        context)

    row = cursor.fetchone()

    return row[0]


def get_project_part_list_sb(project):
    '''given a project,
 return all parts with risk_level = H or annual PVO > 250KEUR'''

    all_parts = get_project_part_list(project)

    parts_sb = []

    for part in all_parts:
        if (get_part_pvo(project, part) > LOCAL_SB_THRESHOLD
                or get_part_risk(project, part) == 'H'):
            parts_sb.append(part)

    return parts_sb


def get_part_volume_avg(project, part):
    '''get part volume average'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT avg(volume) AS vol_avg FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? AND RP.volume != 0''', context)

    rc = cursor.fetchone()
    if rc:
        return rc['vol_avg']
    else:
        return None


def get_quotation_yearly_info(project, part, vendor):
    '''get yearly price as part of quoation dict'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute(
        '''SELECT price100, qs FROM nomi_part AS NP
              WHERE NP.project=? AND NP.part=? AND NP.vendor=?''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return result


def get_quotation_invest_info(project, part, vendor):
    '''get yearly price as part of quoation dict'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute(
        '''SELECT * FROM rfq_invest LEFT JOIN nomi_invest AS NI
        USING (project, part, vendor, tool)
        WHERE NI.project=? AND NI.part=? AND NI.vendor=? ORDER BY tool''',
        context)

    rows = cursor.fetchall()
    return rows


def get_vendor_list_under_part(project, part):
    '''get vendor list (supplier selected) for project x part'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT DISTINCT vendor FROM sourcing_concept
                        WHERE project=? AND part=? ORDER BY vendor''', context)

    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_part_list_by_project(project):
    '''given a project,
 return a list with all parts by search the part_data sheet'''
    cursor = CONN_f.cursor()
    context = (project, )
    cursor.execute(
        '''SELECT DISTINCT part FROM part_data
        WHERE project=? ORDER BY part''', context)
    rows = cursor.fetchall()
    part_list = [item[0] for item in rows]
    return part_list


def get_part_list_by_project_vendor(project, vendor):
    '''function for nl_generate in route module'''

    cursor = CONN.cursor()
    context = (project, vendor)

    cursor.execute(
        '''SELECT DISTINCT part FROM nomi_part
                        WHERE project=? AND vendor=? ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [row[0] for row in rows]

    return result


def get_part_timing(project, part):
    '''get all fields from project timing sheet'''

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        '''SELECT * FROM project_timing
                        WHERE project=? AND part=? ORDER BY part''', context)

    row = cursor.fetchone()
    return row


def get_all_project_list():
    '''used for all projects test'''

    cursor = CONN.cursor()
    cursor.execute('''SELECT DISTINCT * FROM project_data''')

    rows = cursor.fetchall()
    project_list = [row[0] for row in rows]

    return project_list
