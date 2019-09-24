'''build dict by sql query and factory'''
import sqlite3
import openpyxl
from collections import defaultdict

from pur_doc.constant import DB_URL, EX_RATE, LOCAL_SB_THRESHOLD
# DB_URL = './data/nr.db'

CONN = sqlite3.connect(DB_URL, check_same_thread=False)

# build a default dict type whoes default value is itself
class myDefaultDict(defaultdict):
    __repr__ = dict.__repr__

def rec_dd():
    return myDefaultDict(rec_dd)


def dict_factory_single_row(cursor, row):
    '''used to build dictionary with data tiltle and data value.
    use cursor.description as iterable and build a dict with titile and value'''

    result = rec_dd()

    for id_num, col in enumerate(cursor.description):
        if row:
            _value = row[id_num] 
            if _value:
                result[col[0]] = _value
            else:
                result[col[0]] = "Undefined"
        else:
            result[col[0]] = "Undefined"

    return result


def dict_factory_multi(cursor, rows, title):
    '''build dict for each part/year/invest with multi rows data'''

    result = rec_dd()

    for id_num, value in enumerate(rows, start=1):
        for num, tuple in enumerate(cursor.description):
            key_name = tuple[0] + '_' + title + '_' + str(id_num) 
            val = value[num]

            result[key_name] = val
    
    return result

def assemble_nl_info(project, vendor, part_list):

    result = rec_dd()
    result['vendor'] = get_vendor_info(vendor)
    result['project'] = get_project_info(project)

    quotation = rec_dd()
    part_info = rec_dd()
    volume_in_1000 = rec_dd()
    volume_in_week = rec_dd()
    invest = rec_dd()

    for id, part in enumerate(part_list, start=1):
        quotation['part_' + str(id)] = assemble_quotation_single_vendor(project, part, vendor)
        part_info['part_' + str(id)] = get_part_general_info(project, part)
        volume_in_1000['part_' + str(id)] = get_part_volume_in1000(project, part)
        volume_in_week['part_' + str(id)] = get_part_volume_inweek(project, part, vendor)
        invest['part_' + str(id)] = get_part_invest_target(project, part)
        
    result['quotation'] = quotation
    result['part_info'] = part_info
    result['kvol'] = volume_in_1000 #use vol to short word length in word...
    result['wvol'] = volume_in_week #use vol to short word length in word...
    result['invest'] = invest

    return result



def assemble_project(project, part_list):

    result = rec_dd()
    
    result['parts'] = assemble_parts_for_project(project, part_list)

    result['project'] = get_project_info(project)

    result['project']['part_list'] = part_list

    result['vendors'] = assemble_vendors(project) # later use part_list as 2nd para, then reduce the vendors list

    return result

def assemble_vendors(project):
    '''assemble all vendor info for the vendor list'''

    vendor_list = get_vendor_list(project)

    result = rec_dd()

    for vendor in vendor_list:
        vendor_info = get_vendor_info(vendor)
        result[str(vendor)] = vendor_info
    
    return result


def assemble_parts_for_project(project, part_list):
    '''use the user chosen part_list as part list'''

    result = rec_dd()

    for part_id, part_number in enumerate(part_list, start=1):
        key_name = 'part_' + str(part_id)
        result[key_name] = assemble_single_part(project, part_number)

    return result


def assemble_single_part(project, part):
    '''assemble the dict for single part'''

    result = rec_dd()

    result['general_info'] = get_part_general_info(project, part)
    result['volume'] = get_part_volume(project, part)
    result['target_price'] = get_part_target_price(project, part)
    result['invest_target'] = get_part_invest_target(project, part)
    result['timing'] = get_part_timing(project, part)
    result['vendor_list'] = get_vendor_list_4part(project, part)
    result['vendor_dict'] = get_vendor_by_part_in_dict(project, part)

    # sovle volume exception:   
    if result['general_info'] and result['volume']:

        result['general_info']['part_life_time'] = len(result['volume'])
        result['general_info']['volume_avg'] = int(sum(result['volume'].values()) / result['general_info']['part_life_time'])
        result['general_info']['target_price100_EUR'] = result['target_price']['target_price100_year_1'] / EX_RATE['EUR'] #result['general_info']['currency']]
        result['general_info']['pvo'] = get_part_pvo(project, part)

    result['quotations'] = assemble_quotation_single_part(project, part)

    return result


def assemble_quotation_single_vendor(project, part, vendor):
    '''assemble all quotaiton sub components'''

    result = rec_dd()

    result['vendor'] = str(vendor)
    result['prices'] = get_quotation_yearly_info(project, part, vendor)
    result['invests'] = get_quotation_invest_info(project, part, vendor)
    result['pvo'] = get_part_quotation_pvo(project, part, vendor)
    result['qs'] = get_part_quotation_qs(project, part, vendor)

    return result

def assemble_quotation_single_part(project, part):
    ''' get quotations from different vendors for a given project and part'''

    # prepare vendor list for this part

    vendor_list = get_vendor_list_4part(project, part)

    result = rec_dd()

    for id, vendor in enumerate(vendor_list, start=1):
        result['vendor_' + str(id)] = assemble_quotation_single_vendor(project, part, vendor)

    return result


def get_part_volume_inweek(project, part, vendor):
    '''get part volume devided by weeks_per_year of vendor and mulitiply 1.3''' 

    cursor = CONN.cursor()
    context = (vendor, )

    # get wpy of vendor
    cursor.execute('''SELECT weeks_per_year AS wpy FROM vendor_production AS VP
              WHERE VP.vendor=?''', context)

    row = cursor.fetchone()
    # print(row)

    if row and type(row[0]) == int:

        wpy = float(row[0])

        context2 = (wpy, project, part)

        cursor.execute('''SELECT ROUND(RP.volume/1000/?*1.3,2) AS vol FROM rfq_part AS RP
                WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context2)

        rows = cursor.fetchall()

        result = dict_factory_multi(cursor, rows, 'y')

        return result

    else:

        print("No weeks_per_year info for this vendor")
        _ = rec_dd()
        return _


def get_part_volume_in1000(project, part):
    '''get part volume in unit K''' 

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT RP.volume/1000 AS vol FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'y')

    return(result)


def get_part_volume(project, part):
    '''get part volume''' 

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT RP.volume FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return(result)

def get_part_target_price(project, part):
    '''get part target price''' 

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT DISTINCT RP.target_price100 FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return(result)
    
def get_part_invest_target(project, part):
    ''''''
    cursor = CONN.cursor()
    context = (project, part)


    cursor.execute('''SELECT DISTINCT *
              FROM rfq_invest AS RI
              WHERE RI.project=? AND RI.part=? ORDER BY RI.tool''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'tool')

    return(result)



def get_part_general_info(project, part):
    '''return a dictionary with titles and values about part general info
    (eg. part_description/mtl_group/etc) based on single part number (not project info involved)'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT DISTINCT * FROM part_data AS pd LEFT JOIN mgs USING(mtl_group)
                   WHERE pd.project=? AND pd.part=?''', context)

    row = cursor.fetchone()

    result = dict_factory_single_row(cursor, row)

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


def get_vendor_list(project):
    '''prepare a list of vendors, whick later quotation of each part can refer to '''

    cursor = CONN.cursor()
    context = (project,)

    cursor.execute('''SELECT DISTINCT vendor FROM sourcing_concept WHERE project=? ORDER BY vendor''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result


def get_nominated_vendor(project, part):
    '''check the sourcing_concept which supplier is marked as nominated'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT DISTINCT vendor FROM sourcing_concept WHERE project=? AND part=? AND vendor_nominated='X' ORDER BY vendor''', context)

    row = cursor.fetchone()

    result = row[0] if row else None

    return result


def get_vendor_info(vendor):
    '''get all general vendor info'''

    cursor = CONN.cursor()
    context = (vendor,)

    cursor.execute('''SELECT * FROM 
    vendor_contact AS VC
    LEFT JOIN vendor_basic AS VB ON VC.vendor=VB.vendor 
    LEFT JOIN contract AS C ON VC.vendor=C.vendor
    LEFT JOIN quality AS Q ON VC.vendor=Q.vendor
    LEFT JOIN vendor_production AS P on VC.vendor=P.vendor
    WHERE VC.vendor=?''', context)

    row = cursor.fetchone()

    result = dict_factory_single_row(cursor, row)
    return result


def get_project_info(project):
    '''return combined project info in one dict from sheets: project_data and project_info'''
    cursor = CONN.cursor()
    context = (project,)

    cursor.execute(
        '''SELECT * FROM project_data LEFT JOIN project_info USING (project) 
            LEFT JOIN plant USING (plant) WHERE project=?''', context)

    # return one row
    row = cursor.fetchone()

    result = dict_factory_single_row(cursor, row)
    return result


def get_project_part_list(project):
    '''given a project, return a list with all parts by search the part_data sheet'''

    cursor = CONN.cursor()
    context = (project, )

    cursor.execute(
        '''SELECT DISTINCT part FROM part_data WHERE project=? ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]

    return result


def get_part_quotation_qs(project, part, vendor):
    '''get total quick saving for a quotation'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute(
        '''SELECT SUM(qs) FROM nomi_part WHERE project=? AND part=? AND vendor=?''', context)

    row = cursor.fetchone()
    result = row[0] or 0

    return result

def get_part_quotation_pvo(project, part, vendor):
    '''return PVO by project and part and vendor'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    # get price pvo
    cursor.execute('''SELECT SUM(year_PVO) FROM (SELECT project, part, year, volume*price100/100 AS year_PVO FROM rfq_part NATURAL JOIN nomi_part WHERE project=? AND part=? AND vendor=?)''', context)

    row = cursor.fetchone()

    part_pvo = row[0] if row[0] else 0

    cursor.execute('''SELECT SUM(invest_cost) FROM (SELECT tool_cost+further_invest_cost AS invest_cost FROM nomi_invest WHERE project=? AND part=? AND vendor=?)''', context)

    row = cursor.fetchone()

    invest_pvo = row[0] if row[0] else 0

    # pvo = (part_pvo + invest_pvo) / EX_RATE['EUR']
    pvo = part_pvo + invest_pvo

    return int(pvo)


def get_part_pvo(project, part):
    '''return PVO by project and part'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT SUM(year_PVO) FROM (SELECT volume*target_price100/100 AS year_PVO FROM rfq_part WHERE project=? AND part=?)''', context)

    row = cursor.fetchone()
    part_pvo = row[0] if row[0] else 0

    cursor.execute('''SELECT SUM(invest_target) FROM (SELECT cost_target+further_invest_cost AS invest_target FROM rfq_invest WHERE project=? AND part=?)''', context)

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
        '''SELECT risk_level FROM part_data WHERE project=? AND part=?''', context)

    row = cursor.fetchone()

    return row[0]


def get_project_part_list_sb(project):
    '''given a project, return all parts with risk_level = H or annual PVO > 250KEUR'''

    all_parts = get_project_part_list(project)

    parts_sb = []

    for part in all_parts:
        if (get_part_pvo(project, part) > LOCAL_SB_THRESHOLD or get_part_risk(project, part) == 'H'):
            parts_sb.append(part)

    return parts_sb


def get_part_volume_4project(project, part):
    '''get part volume average'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT avg(volume) AS vol_avg FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ''', context)

    row = cursor.fetchone()

    return int(row[0])

def get_quotation_yearly_info(project, part, vendor):
    '''get yearly price as part of quoation dict'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute('''SELECT price100, qs FROM nomi_part AS NP 
              WHERE NP.project=? AND NP.part=? AND NP.vendor=?''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return result

def get_quotation_invest_info(project, part, vendor):
    '''get yearly price as part of quoation dict'''

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute('''SELECT cavity, tool_cost, copy_tool_cost, further_invest_cost, nomi_ppap_date, nomi_fot_date, nomi_loops
                     FROM nomi_invest AS NI WHERE NI.project=? AND NI.part=? AND NI.vendor=? ORDER BY tool''', context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'tool')

    return result


def get_vendor_list_4part(project, part):
    '''get vendor list for project x part'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT DISTINCT vendor FROM sourcing_concept 
                        WHERE project=? AND part=? ORDER BY vendor''', context)

    rows = cursor.fetchall()
    result = [item[0] for item in rows]
    
    nominated_vendor = get_nominated_vendor(project, part)
    
    if nominated_vendor:
        a = result.index(nominated_vendor)
        temp = result[0]
        result[0] = nominated_vendor
        result[a] = temp

    return result

def get_part_list_by_project_vendor(project, vendor):
    '''function for nl_generate in route module'''

    cursor = CONN.cursor()
    context = (project, vendor)

    cursor.execute('''SELECT DISTINCT part FROM nomi_part 
                        WHERE project=? AND vendor=? ORDER BY part''', context)

    rows = cursor.fetchall()
    result = [row[0] for row in rows]

    return result

def get_part_timing(project, part):
    '''get all fields from project timing sheet'''

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute('''SELECT * FROM project_timing 
                        WHERE project=? AND part=? ORDER BY part''', context)

    row = cursor.fetchone()
    result = dict_factory_single_row(cursor, row)

    return result

def get_vendor_by_part_in_dict(project, part):
    '''xxx'''

    result = rec_dd()

    vendor_list = get_vendor_list_4part(project, part)
    for id, vendor in enumerate(vendor_list, start=1):
        result['vendor_' + str(id)] = vendor_list[id - 1]

    return result

