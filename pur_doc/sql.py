'''build dict by sql query and factory'''
import sqlite3
import openpyxl

from pur_doc.constant import DB_URL, EX_RATE, LOCAL_SB_THRESHOLD
# DB_URL = './data/nr.db'

CONN = sqlite3.connect(DB_URL, check_same_thread=False)


def dict_factory_single_row(cursor, row):
    '''used to build dictionary with data tiltle and data value.
    use cursor.description as iterable and build a dict with titile and value'''
    result = {}
    for id_num, col in enumerate(cursor.description):
        result[col[0]] = row[id_num]
    return result


def dict_factory_single_col(curosr, rows, title):
    '''produce the dict with title+id. eg: year_1, year_2, year_3...'''

    pass


def dict_factory_multi(cursor, rows, title):
    '''coursor contains title information
        rows is the data
        title is name you want to give them'''
    result = {}
    for id, row in enumerate(rows):
        result[title + '_' + str(id)] = dict_factory_single_row(cursor, row)
    return result


def search_part_combine(project, vendor):
    '''find the part list, search part info one by one and combine to a big
    list'''

    part_list = search_pn(project, vendor)  # return list of pns
    result = {}  # final combined dict/json to front-end
    part_info = {}  # helper dict/container to gether part_info

    # build part_info
    for id_num, part in enumerate(part_list):
        mtl = search_part_description(part)
        yearly = search_year_info(project, vendor, part)
        invest = search_invest_info(project, vendor, part)
        part_info['part' + str(id_num)] = dict(mtl=mtl,
                                               yearly=yearly,
                                               invest=invest)

    result['part'] = part_info
    result['vendor'] = get_vendor_info(vendor)
    result['project'] = search_project_info(project)

    return result

def combine_output_by_project_and_vendor(project, vendor):
    '''output the whole dict for one project'''

    pass


def combine_output_by_project_and_vendor_and_parts(project, vendor, part_list):
    '''output the whole dict for one project'''

    pass

def combined_output(project, part, vendor):
    '''
    output the whole dict for one project
    include:
    - project
        - all information
    - parts
        - part1
            - general info
            - part_vol/target price (from rfq)
            - quotations
                - vendor1
                    - vendor_info(vendor, name, contracts and contacts)
                    - prices
                    - xxx
                - vendor2
        - part2 
    (optional)
    - part_list
    - part_list_4sb
    - vendor_list
    '''


    part_list = get_project_part_list(project) # return list of all parts

    project = get_project_info(project)  # helper dict/container to gether part_info

    result = {}  # final combined dict/json to front-end

    # build part_info
    for id_num, part in enumerate(part_list):
        mtl = search_part_description(part)
        yearly = search_year_info(project, vendor, part)
        invest = search_invest_info(project, vendor, part)
        part_info['part' + str(id_num)] = dict(mtl=mtl,
                                               yearly=yearly,
                                               invest=invest)

    result['part'] = part_info
    result['vendor'] = get_vendor_info(vendor)
    result['project'] = search_project_info(project)

    return result

def get_quotation_prices(project, part, vendor):
    '''get prices info''' 

    cursor = CONN.cursor()
    context = (project, vendor, part)

    cursor.execute('''SELECT DISTINCT RP.part, RP.year, RP.volume, NP.vendor,
              NP.price100,NP.qs FROM rfq_part AS RP
              LEFT JOIN nomi_part AS NP ON RP.project=NP.project AND
              RP.part=NP.part AND RP.year=NP.year WHERE RP.project=?
              AND NP.vendor=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    


def get_part_general_info(part):
    '''return a dictionary with titles and values about part general info
    (eg. part_description/mtl_group/etc) based on single part number (not project info involved)'''

    cursor = CONN.cursor()
    context = (part,)

    cursor.execute('''SELECT DISTINCT * FROM part_data AS pd LEFT JOIN mgs USING(mtl_group)
                   WHERE pd.part=?''', context)

    row = cursor.fetchone()

    result = dict_factory_single_row(cursor, row)

    return result


def search_year_info(project, vendor, part):
    '''find year related info based on the given project/vendor/part'''

    cursor = CONN.cursor()
    context = (project, vendor, part)
    print(context)

    cursor.execute('''SELECT DISTINCT RP.part, RP.year, RP.volume, NP.vendor,
              NP.price100,NP.qs FROM rfq_part AS RP
              LEFT JOIN nomi_part AS NP ON RP.project=NP.project AND
              RP.part=NP.part AND RP.year=NP.year WHERE RP.project=?
              AND NP.vendor=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()
    print(rows)

    result = dict_factory_multi(cursor, rows, 'year')

    return result


def search_invest_info(project, vendor, part):
    '''fine invest info based on given pn'''
    cursor = CONN.cursor()
    context = (project, vendor, part)

    cursor.execute('''SELECT * FROM nomi_invest AS NI WHERE NI.project=? AND
    NI.vendor=? AND NI.part=? ORDER BY NI.tool''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'invest')

    return result


def get_vendor_info(vendor):
    '''get all general vender info'''

    cursor = CONN.cursor()
    context = (vendor,)

    cursor.execute('''SELECT * FROM vendor_basic AS VB
    NATURAL JOIN vendor_contact AS VC 
    NATURAL JOIN contract AS C
    NATURAL JOIN quality AS Q
    WHERE vendor=?''', context)

    row = cursor.fetchone()

    if row:
        result = dict_factory_single_row(cursor, row)
        return result
    return None


def get_project_info(project):
    '''return combined project info in one dict from sheets: project_data and project_info'''
    cursor = CONN.cursor()
    context = (project,)

    cursor.execute(
        '''SELECT * FROM project_info LEFT JOIN project_data USING (project) WHERE project=?''', context)

    # return one row
    row = cursor.fetchone()

    if row:
        result = dict_factory_single_row(cursor, row)
        return result
    return {}


def get_project_part_list(project):
    '''given a project, return a list with all parts'''

    cursor = CONN.cursor()
    context = (project, )

    cursor.execute(
        '''SELECT DISTINCT part FROM sourcing_concept WHERE project=? ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result


def get_part_pvo(project, part):
    '''return PVO by project and part'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT SUM(year_PVO) FROM (SELECT volume*target_price100/100 AS year_PVO FROM rfq_part WHERE project=? AND part=?) GROUP BY year_PVO''', context)

    row = cursor.fetchone()

    pvo = row[0] / EX_RATE['EUR']

    return int(pvo)


def get_part_risk(part):
    '''get risk level'''

    cursor = CONN.cursor()
    context = (part,)

    cursor.execute(
        '''SELECT risk_level FROM part_data WHERE part=?''', context)

    row = cursor.fetchone()

    return row[0]


def get_project_part_list_4sb(project):
    '''given a project, return all parts with risk_level = H or annual PVO > 250KEUR'''

    all_parts = get_project_part_list(project)

    parts_4sb = []

    for part in all_parts:
        if (get_part_pvo(project, part) > LOCAL_SB_THRESHOLD and get_part_risk(part) == 'H'):
            parts_4sb.append(part)

    return parts_4sb


def get_part_volume_4project(project, part):
    '''return all the part info related to certain part in certain project into a dict'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT DISTINCT volume FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return result
