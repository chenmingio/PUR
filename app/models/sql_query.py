"""build dict by sql query and factory"""
import sqlite3
from collections import defaultdict
from pprint import pprint
import json

import config

CONN = sqlite3.connect(config.SQLITE_DATABASE_URI, check_same_thread=False)
CONN_f = sqlite3.connect(config.SQLITE_DATABASE_URI, check_same_thread=False)

CONN_f.row_factory = sqlite3.Row

# Remind word for missing info
REMIND_WORD = 'None'
DEFAULT_WPY = 50


def constant_factory():
    """used for defaultdict return"""
    return REMIND_WORD


def get_project_sop_eop(project):
    """find the min/max year number in rfq_part year column where the quantity
    is not 0 as real SOP/EOP year"""

    cursor = CONN_f.cursor()
    context = (project,)

    cursor.execute(
        """SELECT MIN(year) AS sop, MAX(year) AS EOP FROM rfq_part
              WHERE project=? AND volume > 0""", context)

    return cursor.fetchone()


def get_vendor_weeks_per_year(vendor):
    cursor = CONN_f.cursor()
    context = (vendor,)

    # get week per year of vendor
    cursor.execute(
        """SELECT weeks_per_year AS wpy FROM vendor_production AS VP
              WHERE VP.vendor=?""", context)

    row = cursor.fetchone()
    if row:
        return row['wpy']


def get_part_volume_weekly(project, part, vendor):
    """get part volume devided by weeks_per_year of vendor and mulitiply 1.3"""

    wpy = get_vendor_weeks_per_year(vendor)

    if wpy is None or wpy.isdigit() is False:
        wpy = DEFAULT_WPY

    temp_dict = get_part_volume_yearly(project, part)
    for vol in temp_dict:
        vol = vol / wpy

    return temp_dict


def get_part_price_yearly(project, part, vendor):
    """get part price. Output a defaultdict (year: price).
    Later when using year outside part lifetime, defaultdict return none instead """

    cursor = CONN_f.cursor()
    context = (project, part, vendor)

    cursor.execute(
        """SELECT year AS year, price100 AS price100 FROM nomi_part AS NP
              WHERE project=? AND part=? AND vendor=? ORDER BY year""", context)

    rows = cursor.fetchall()

    part_price_dict = defaultdict(constant_factory)

    if rows:
        for row in rows:
            year = row['year']
            price100 = row['price100']
            part_price_dict[year] = price100

    return part_price_dict


def get_part_volume_yearly(project, part):
    """get part volume. Output a defaultdict (year: vol).
    Later when using year outside part lifetime, defaultdict return none instead """

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT RP.year AS year, RP.volume AS vol FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year""", context)

    rows = cursor.fetchall()

    part_vol_dict = defaultdict(constant_factory)

    if rows:
        for row in rows:
            if isinstance(row['vol'], int) or isinstance(row['vol'], float):
                year = row['year']
                vol = row['vol']
                part_vol_dict[year] = vol

    print(part_vol_dict)
    return part_vol_dict


def get_part_volume_sum(project, part):
    """get part volume"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT SUM(volume) AS vol_sum FROM rfq_part
              WHERE project=? AND part=?""", context)

    row = cursor.fetchone()
    if row:
        return row['vol_sum']


def get_part_target_price_avg_100EUR(project, part):
    pvo_part = get_part_target_pvo_part(project, part)
    lifetime = get_part_lifetime(project, part)
    vol_sum = get_part_volume_sum(project, part)

    if pvo_part and lifetime and vol_sum:
        target_price = pvo_part / lifetime / vol_sum / config.EX_RATE['EUR'] * 100
        return target_price


def get_part_target_price(project, part):
    """get part target price"""

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT DISTINCT RP.target_price100 FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? ORDER BY RP.year""", context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return result


def get_part_invest_target(project, part):
    """"""
    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT DISTINCT *
              FROM rfq_invest AS RI
              WHERE RI.project=? AND RI.part=? ORDER BY RI.tool""", context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'tool')

    return (result)


def get_part_general_info(project, part):
    """return a dictionary with titles and values about part general info
    (eg. part_description/mtl_group/etc,)
    based on single part number
    (project info also involved for nr_id cross location)"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT DISTINCT * FROM part_data AS pd
        LEFT JOIN mgm USING(mtl_group)
        LEFT JOIN mgs_sqe USING(mtl_group)
        LEFT JOIN plant USING(plant)
        WHERE pd.project=? AND pd.part=?""", context)

    return cursor.fetchone()


def search_invest_info(project, vendor, part):
    """fine invest info from rfq_invest and nomi_invest  based on given pn"""
    cursor = CONN.cursor()
    context = (project, vendor, part)

    cursor.execute(
        """SELECT * FROM nomi_invest AS NI WHERE NI.project=? AND
    NI.vendor=? AND NI.part=? ORDER BY NI.tool""", context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'invest')

    return result


def get_vendor_list_by_project(project):
    """prepare a list of vendors"""

    cursor = CONN_f.cursor()
    context = (project,)

    cursor.execute(
        """SELECT DISTINCT vendor FROM sourcing_concept WHERE project=? ORDER
        BY vendor""", context)

    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_nominated_vendor(project, part):
    """check the sourcing_concept which supplier is marked as nominated"""

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT DISTINCT vendor FROM sourcing_concept WHERE project=?
        AND part=? AND vendor_nominated='X' ORDER BY vendor""", context)

    row = cursor.fetchone()

    result = row[0] if row else None

    return result


def get_vendor_info(vendor):
    """get all general vendor info"""

    cursor = CONN_f.cursor()
    context = (vendor,)

    cursor.execute(
        """SELECT * FROM
    vendor_contact AS VC
    LEFT JOIN vendor_basic AS VB ON VC.vendor=VB.vendor
    LEFT JOIN contract AS C ON VC.vendor=C.vendor
    LEFT JOIN quality AS Q ON VC.vendor=Q.vendor
    LEFT JOIN vendor_production AS P on VC.vendor=P.vendor
    WHERE VC.vendor=?""", context)

    row = cursor.fetchone()

    if row:
        return row
    else:
        return None


def get_project_data_and_info(project):
    """from TABLE: project_data + project_info"""
    cursor = CONN_f.cursor()
    context = (project,)
    cursor.execute(
        """SELECT * FROM project_data LEFT JOIN project_info USING (project)
            LEFT JOIN plant USING (plant) WHERE project=?""", context)
    row = cursor.fetchone()
    return row


def get_project_vendor_qs_yearly(project, vendor):
    """return a (year-qs) tuple list"""

    cursor = CONN_f.cursor()
    context = (project, vendor)

    cursor.execute(
        """SELECT year, SUM(qs) AS qs 
        FROM nomi_part 
        WHERE project=? AND vendor=? AND qs>0
        GROUP BY year""", context)

    rows = cursor.fetchall()
    return [(row['year'], row['qs']) for row in rows]


def get_part_quotation_pvo(project, part, vendor):
    """return PVO by project and part and vendor"""

    cursor = CONN.cursor()
    context = (project, part, vendor)

    # get price pvo
    cursor.execute(
        """SELECT SUM(year_PVO) FROM (SELECT project, part, year, volume*price100/100 AS year_PVO 
        FROM rfq_part NATURAL JOIN nomi_part
        WHERE project=? AND part=? AND vendor=?,
)""", context)

    row = cursor.fetchone()

    part_pvo = row[0] if row[0] else 0

    cursor.execute(
        """SELECT SUM(invest_cost,) FROM
        (SELECT tool_cost+further_invest_cost AS invest_cost FROM nomi_invest
        WHERE project=? AND part=? AND vendor=?,
)""", context)

    row = cursor.fetchone()

    invest_pvo = row[0] if row[0] else 0

    # pvo = (part_pvo + invest_pvo) / EX_RATE['EUR']
    pvo = part_pvo + invest_pvo

    return int(pvo)


def get_part_target_pvo_part(project, part):
    """PVO target only for parts"""
    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT SUM(year_PVO) AS target_pvo_part FROM
        (SELECT volume*target_price100/100 AS year_PVO FROM rfq_part
        WHERE project=? AND part=?)""", context)

    row = cursor.fetchone()
    if row:
        return row['target_pvo_part']
    else:
        return None


def get_part_target_pvo_investment(project, part):
    """PVO target only for investment"""
    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT SUM(invest_target) AS invest_target_pvo
        FROM (
            SELECT cost_target+further_invest_cost AS invest_target
                FROM rfq_invest
            WHERE project=? AND part=?)""", context)

    row = cursor.fetchone()
    if row:
        return row['invest_target_pvo']
    else:
        return None


def get_part_target_pvo_total(project, part):
    """add target pvo of part and investment together"""
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
    """real lifetime according to row with volume from TABLE rfq_part"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT COUNT(*) AS count
        FROM rfq_part WHERE project=? AND part=?""", context)
    row = cursor.fetchone()
    if row:
        return row['count']


def get_part_pvo(project, part):
    """return PVO by project and part"""

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT SUM(
year_PVO,
) FROM (
SELECT volume*target_price100/100 AS year_PVO FROM rfq_part
        WHERE project=? AND part=?,)""", context)

    row = cursor.fetchone()
    part_pvo = row[0] if row[0] else 0

    cursor.execute(
        """SELECT SUM(
invest_target,
) FROM (
SELECT cost_target+further_invest_cost AS invest_target FROM rfq_invest
        WHERE project=? AND part=?,)""", context)

    row = cursor.fetchone()

    invest_pvo = row[0] if row[0] else 0

    # pvo = (part_pvo + invest_pvo) / EX_RATE['EUR']
    pvo = part_pvo + invest_pvo

    return int(pvo)


def get_part_risk(project, part):
    """get risk level"""

    cursor = CONN.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT risk_level FROM part_data WHERE project=? AND part=?""",
        context)

    row = cursor.fetchone()

    return row[0]


def get_project_part_list_sb(project):
    """given a project,
 return all parts with risk_level = H or annual PVO > 250KEUR"""

    all_parts = get_project_part_list(project)

    parts_sb = []

    for part in all_parts:
        if (get_part_pvo(project, part) > config.LOCAL_SB_THRESHOLD
                or get_part_risk(project, part) == 'H'):
            parts_sb.append(part)

    return parts_sb


def get_part_volume_avg(project, part):
    """get part volume average"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT avg(volume) AS vol_avg FROM rfq_part AS RP
              WHERE RP.project=? AND RP.part=? AND RP.volume != 0""", context)

    rc = cursor.fetchone()
    if rc:
        return rc['vol_avg']
    else:
        return None


def get_quotation_yearly_info(project, part, vendor):
    """get yearly price as part of quotation dict"""

    cursor = CONN.cursor()
    context = (project, part, vendor)

    cursor.execute(
        """SELECT price100, qs FROM nomi_part AS NP
              WHERE NP.project=? AND NP.part=? AND NP.vendor=?""", context)

    rows = cursor.fetchall()

    result = dict_factory_multi(cursor, rows, 'year')

    return result


def get_nl_tool_info(project, vendor, part_list):
    """get all fields from rfq_invest table and nomi_invest table
    about the tooling, return within a row list"""

    cursor = CONN_f.cursor()
    context = (project, vendor, *part_list)

    placeholders = ','.join('?' * len(part_list))
    query = f"""SELECT DISTINCT * 
                    FROM rfq_invest LEFT JOIN nomi_invest AS NI
                USING (project, part, tool)
                WHERE NI.project=? AND NI.vendor=? AND NI.part IN ({placeholders})
                ORDER BY part, tool"""

    cursor.execute(query, context)

    rows = cursor.fetchall()
    return rows


def get_nl_invest_info(project, vendor, part_list):
    """same as nl_tool_info function"""

    cursor = CONN_f.cursor()
    context = (project, vendor, *part_list)

    placeholders = ','.join('?' * len(part_list))
    query = f"""SELECT DISTINCT
                    RI.part AS part, RI.further_invest_name AS invest_name, NI.further_invest_cost AS cost
                FROM rfq_invest  AS RI LEFT JOIN nomi_invest AS NI
                USING (project, part, tool)
                WHERE NI.project=? AND NI.vendor=? AND NI.part IN ({placeholders}) AND invest_name IS NOT NULL
                ORDER BY part, tool"""

    cursor.execute(query, context)

    rows = cursor.fetchall()
    return rows


def get_vendor_list_under_part(project, part):
    """get vendor list (supplier selected) for project x part"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT DISTINCT vendor FROM sourcing_concept
                        WHERE project=? AND part=? ORDER BY vendor""", context)

    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_part_list_by_project(project):
    """given a project,
 return a list with all parts by search the part_data sheet"""
    cursor = CONN_f.cursor()
    context = (project,)
    cursor.execute(
        """SELECT DISTINCT part FROM part_data
        WHERE project=? ORDER BY part""", context)
    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_part_list_by_project_vendor(project, vendor):
    """function for nl_generate in route module"""

    cursor = CONN_f.cursor()
    context = (project, vendor)

    cursor.execute(
        """SELECT DISTINCT part FROM nomi_part
                WHERE project=? AND vendor=? ORDER BY part""", context)

    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_part_timing(project, part):
    """get all fields from project timing sheet"""

    cursor = CONN_f.cursor()
    context = (project, part)

    cursor.execute(
        """SELECT * FROM project_timing
                        WHERE project=? AND part=? ORDER BY part""", context)

    row = cursor.fetchone()
    return row


def get_all_project_list():
    """used for all projects test"""

    cursor = CONN.cursor()
    cursor.execute("""SELECT DISTINCT * FROM project_data""")

    rows = cursor.fetchall()
    project_list = [row[0] for row in rows]

    return project_list


def get_all_project_vendor_tuple():
    """get (project, vendor) tuple for nl test """

    cursor = CONN_f.cursor()
    cursor.execute(
        """SELECT DISTINCT project, vendor FROM nomi_part"""
    )

    rows = cursor.fetchall()
    return [(row['project'], row['vendor']) for row in rows]


def create_project_info_table():
    """create a table into sqlite DB of project info, which is more precise than pandas auto loading."""

    cursor = CONN_f.cursor()
    cursor.execute('''
        CREATE TABLE "project_info" (
	    "project"	TEXT NOT NULL UNIQUE,
	    "product_group" TEXT,
	    "project_name"	TEXT,
	    "customer" TEXT,
	    "car" TEXT,
	    "mdb_status" TEXT,
	    "project_status" TEXT,
	    "dd_location" TEXT,
	    "production_line" TEXT,
	    "fg_part_number" TEXT,
	    "production_cycle_time" TEXT,
	    "budget_available" TEXT,
	    "sop_hella_date" DATE,
	    "run_rate_hella_date" DATE,
	    "pv_hella_date" DATE,
	    "sop_customer_date" DATE,
	    "pjm" TEXT,
	    "app" TEXT,
	    "md" TEXT,
	    "controlling" TEXT,
	    "sqa" TEXT,
	    "logistic" TEXT,
	    "me" TEXT,
	    PRIMARY KEY("project")
            );
    ''')

    CONN_f.commit()


def create_part_info_table():
    """create a table into sqlite DB of project info, which is more precise than pandas auto loading."""

    cursor = CONN_f.cursor()
    cursor.execute('''
        CREATE TABLE "part_info" (
	    "project"	TEXT NOT NULL,
	    "part" TEXT,
	    "part_description"	TEXT,
	    "usage" REAL,
	    "target_price" REAL,
	    "target_invest" REAL,
	    "sourcing_date" DATE,
	    "t1_date" DATE,
	    "t2_date" DATE,
	    "t3_date" DATE,
	    "pv_date" DATE,
	    "ppap_date" DATE
            );
             ''')

    CONN_f.commit()


def project_info_save_or_update(project_multidict):
    """save project info into Project INFO table"""

    # TODO: check project id is not null and legit
    # TODO: think about the date/real/integer type risk/problem?
    # add index to volume list

    cursor = CONN_f.cursor()

    # insert/update project basic info. Filter out the list object in dict
    project_tuple_list = [item for item in (project_multidict.items()) if '[]' not in item[0]]
    project_tuple_list_full = [item for item in (project_multidict.items())]

    pprint(f"[save project]: key:value tuple w/ volume&parts : {project_tuple_list_full}")
    pprint(f"[save project]: key:value tuple w/o volume&parts : {project_tuple_list}")

    # build query
    column_list = tuple(key for key, _ in project_tuple_list)

    placeholders = ','.join('?' * len(project_tuple_list))
    context = tuple(val for _, val in project_tuple_list)

    query = f'REPLACE INTO project_info {column_list} VALUES ({placeholders})'
    print("[save project] query: ", query)
    print("[save project] context: ", context)
    cursor.execute(query, context)

    project = project_multidict.get('project')
    if project is False:
        return 0

    # insert demand list into project_volume
    volume_list = project_multidict.getlist('volume_list[]')
    if volume_list:
        print("[save volume] volume list: ", volume_list)
        volume_tuple_list = [(project, num, volume) for num, volume in enumerate(volume_list, start=1) if volume]
        print("[save volume] volume context: ", volume_tuple_list)
        cursor.execute("DELETE FROM project_volume WHERE project=(?)", (project,))
        cursor.executemany('''INSERT INTO project_volume VALUES (?,?,?)''', volume_tuple_list)

    # insert part list into part_info
    # firstly delete existing part records (even if part list is empty, means current part list should be removed
    cursor.execute("DELETE FROM part_info WHERE project=(?)", (project,))

    part_list = project_multidict.getlist('part_list[]')
    if part_list:
        print("[save part] part list: ", part_list)

        # prepare records list
        part_dict_list = [json.loads(dict_string) for dict_string in part_list]
        print("[save part] part_dict_list: ", part_dict_list)

        for part_dict in part_dict_list:
            # make sure part/part-description not both empty
            if part_dict["part"] or part_dict["part_description"]:
                part_dict["project"] = project

                # prepare column names
                part_column_tuple = tuple(part_dict.keys())
                print("[save part] part keys tuple: ", part_column_tuple)
                # prepare placeholders
                placeholders_part = ','.join('?' * len(part_column_tuple))
                # prepare value tuples
                part_value_tuple = tuple(val for _, val in part_dict.items())

                query_part_insert = f'INSERT INTO part_info {part_column_tuple} VALUES ({placeholders_part})'
                cursor.execute(query_part_insert, part_value_tuple)

    CONN_f.commit()

    return 1


def project_info_delete(project):
    """delete project info/project volume/part info related to certain project"""

    cursor = CONN_f.cursor()
    context = (project,)
    cursor.execute("DELETE FROM project_info WHERE project=(?)", context)
    cursor.execute("DELETE FROM project_volume WHERE project=(?)", context)
    cursor.execute("DELETE FROM part_info WHERE project=(?)", context)

    CONN_f.commit()

    return f"project: {project} deleted"


def project_info_get(project):
    """get project info for project_info pages"""

    print("[get project-info]: ", project)
    cursor = CONN_f.cursor()
    context = (project,)
    cursor.execute("SELECT * FROM project_info WHERE project=(?)", context)
    row = cursor.fetchone()
    if row:
        rc = dict(row)

        # get volume list:
        cursor.execute("SELECT * FROM project_volume WHERE project=(?) ORDER BY year", context)
        rows = cursor.fetchall()
        volume_list = [item["volume"] for item in rows]

        rc["volume_list"] = volume_list

        # get part list:
        cursor.execute("SELECT * FROM part_info WHERE project=(?)", context)
        rows = cursor.fetchall()
        part_list = [dict(row) for row in rows]
        # there will be extra "project" key inside part. I put extra optional property "project" inside part type
        print("[get project] part_list: ", part_list)

        rc["part_list"] = part_list

        return rc
