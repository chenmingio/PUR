'''build dict by sql query and factory'''
import sqlite3
import openpyxl

from pur_doc.constant import DB_URL, EX_RATE, LOCAL_SB_THRESHOLD
# DB_URL = './data/nr.db'

CONN = sqlite3.connect(DB_URL, check_same_thread=False)


def dict_factory_single(cursor, row):
    '''use cursor.description as iterable and build a dict with titile and value'''
    result = {}
    for id_num, col in enumerate(cursor.description):
        result[col[0]] = row[id_num]
    return result


def dict_factory_multi(cursor, rows, table):
    '''docstring'''
    result = {}
    for part_id, row in enumerate(rows):
        result[table + str(part_id)] = dict_factory_single(cursor, row)
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
    result['vendor'] = search_vendor_info(vendor)
    result['project'] = search_project_info(project)

    return result


def search_pn(project, vendor):
    '''search part numbers from nomi_part sheet'''

    cursor = CONN.cursor()
    context = (project, vendor)

    cursor.execute('''SELECT DISTINCT part FROM nomi_part WHERE project=? AND
            vendor=? ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result


def search_part_description(part):
    '''return part info(eg. part_description/mtl_group/etc)
        based on single part number'''

    cursor = CONN.cursor()
    context = (part,)

    cursor.execute('''SELECT DISTINCT * FROM part_data AS pd
                   WHERE pd.part=?''', context)

    row = cursor.fetchone()

    result = dict_factory_single(cursor, row)

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


def search_vendor_info(vendor):
    '''docstring'''
    cursor = CONN.cursor()
    context = (vendor,)

    cursor.execute('''SELECT * FROM vendors WHERE vendor=?''', context)

    row = cursor.fetchone()

    if row:
        result = dict_factory_single(cursor, row)
        return result
    return None


def search_project(project):
    '''return combined project info in one dict'''
    cursor = CONN.cursor()
    context = (project,)

    cursor.execute('''SELECT * FROM project_info LEFT JOIN project_data USING (project) WHERE project=?''', context)

    # return one row
    row = cursor.fetchone()

    if row:
        result = dict_factory_single(cursor, row)
        return result
    return {}

def get_part_list_project(project):
    '''given a project, return a list with all parts'''

    cursor = CONN.cursor()
    context = (project, )

    cursor.execute('''SELECT DISTINCT part FROM sourcing_concept WHERE project=? ORDER BY part''', context)

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

    cursor.execute('''SELECT risk_level FROM part_data WHERE part=?''', context)

    row = cursor.fetchone()

    return row[0]


def search_part_list_project_4sb(project):
    '''given a project, return all parts with risk_level = H or annual PVO > 250KEUR'''

    all_parts = get_part_list_project(project)

    parts_4sb = []

    for part in all_parts:
        if (get_part_pvo(project, part) > LOCAL_SB_THRESHOLD and get_part_risk(part) == 'H'):
            parts_4sb.append(part)

    return parts_4sb


def search_part_info(project, part):
    '''return all the part info related to certain part in certain project into a dict'''

    pass
