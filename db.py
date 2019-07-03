'''handle the CRUD function around sqlites db'''
import sqlite3


CONN = sqlite3.connect('nr.db', check_same_thread=False)


def dict_factory_single(cursor, row):
    '''docstring'''
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


def creat_tables():
    ''' docstring '''
    cursor = CONN.cursor()

    # Create table project_ata
    cursor.execute('''CREATE TABLE project_data
                 (project TEXT, plant TEXT, project_name TEXT)''')

    # Create table part_data
    cursor.execute('''CREATE TABLE part_data
                 (project TEXT, nr_id TEXT, part TEXT, part_description TEXT,
                 mtl_group TEXT, raw_mtl TEXT, currency TEXT, risk_level TEXT,
                 buyer TEXT)''')

    # Create table project_timing
    cursor.execute('''CREATE TABLE project_timing
                 (project TEXT, part TEXT, ppap_date TEXT, tooling_weeks TEXT,
                   nomi_date TEXT, rfq_weeks TEXT, drawing_date TEXT)''')

    # Create table sourcing_concept
    cursor.execute('''CREATE TABLE sourcing_concept
                 (project TEXT, part TEXT, vendor TEXT, vendor_nominated TEXT,
                 vendor_active TEXT)''')

    # Create table rfq_part
    cursor.execute('''CREATE TABLE rfq_part
                 (project TEXT, part TEXT, year INTEGER, volume INTEGER,
                 target_price100 REAL)''')

    # Create table rfq_invest
    cursor.execute('''CREATE TABLE rfq_invest
                 (project TEXT, part TEXT, tool INTEGER, tool_description TEXT,
                 cav_target INTEGER, cost_target INTEGER, loop_target TEXT,
                 copy_tool_name TEXT, copy_tool_cost INTEGER,
                 further_invest_name TEXT, further_invest_cost INTEGER)''')

    # Create table nomi_part
    cursor.execute('''CREATE TABLE nomi_part
                 (project TEXT, part TEXT, vendor TEXT, year INTEGER, price100
                 REAL, lta REAL, qs INTEGER, quota REAL)''')

    # Create table nomi_invest
    cursor.execute('''CREATE TABLE nomi_invest
                 (project TEXT, part TEXT, vendor TEXT, tool INTEGER,
                 nomi_date TEXT, cavity INTEGER, tool_cost INTEGER,
                 copy_tool_cost INTEGER, further_invest_cost INTEGER, currency
                 TEXT, nomi_ppap_date TEXT, nomi_fot_date TEXT,
                 nomi_loops TEXT, nomi_letter_signed TEXT)''')

    # Create table vendors
    cursor.execute('''CREATE TABLE vendors
                 (vendor TEXT, vendor_name TEXT, address TEXT, city TEXT,
                 province TEXT, country TEXT, delivery_reg_date TEXT,
                 tool_contract_date TEXT, framework_date TEXT, shifts_per_day
                 INTEGER, shift_duration INTEGER, days_per_week INTEGER,
                 weeks_per_year INTEGER, flex_pre INTEGER, flex_duration
                 INTEGER, flex_froz INTEGER)''')

    # Create table contacts
    cursor.execute('''CREATE TABLE contacts
                 (vendor TEXT, function TEXT, name TEXT, email TEXT,
                 phone TEXT)''')

    # Create table buyers
    cursor.execute('''CREATE TABLE buyers
                 (buyer TEXT, name TEXT, email TEXT,
                 phone TEXT)''')

    CONN.commit()
    CONN.close()


def search_part_combine(project, vendor):
    '''find the part list, search part info one by one and combine to a big
    list'''

    part_list = search_pn(project, vendor)  # return list of pns
    result = {}  # final combined dict/json to front-end
    part_info = {}  # helper dict/container to gether part_info

    # build part_info
    for id_num, part in enumerate(part_list):
        part_info = search_part_description(part)
        year_info = search_year_info(project, vendor, part)
        invest_info = search_invest_info(project, vendor, part)
        part_info['part' + str(id_num)] = result(part_info=part_info,
                                                 year_info=year_info,
                                                 invest_info=invest_info)

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


def search_project_info(project):
    '''docstring'''
    cursor = CONN.cursor()
    context = (project,)

    cursor.execute('''SELECT * FROM project_data WHERE project=?''', context)

    row = cursor.fetchone()

    if row:
        result = dict_factory_single(cursor, row)
        return result
    return {}


def clear_nr(tables):
    ''' docstring '''
    for table in tables:
        cursor = CONN.cursor()

        string = "DELETE FROM " + table
        print(string)

        cursor.execute(string)
        print(table + ' delected.')

    CONN.commit()


if __name__ == "__main__":

    TEST_PROJECT = "1111E.001239"
    TEST_VENDOR = "48200025"
    TEST_PART = "230.033-00"

    print(search_pn(TEST_PROJECT, TEST_VENDOR))
    print(search_project_info(TEST_PROJECT))
    print(search_year_info(TEST_PROJECT, TEST_VENDOR, TEST_PART))
    # print(search_part(project, vendor, part))
    # clear_nr(['vendors', 'contacts', 'buyers'])

    # clear_nr(['project_data', 'part_data', 'project_timing',
    # 'sourcing_concept',
    # 'rfq_part', 'rfq_invest', 'nomi_part', 'nomi_invest'])

    # CONN.close()
