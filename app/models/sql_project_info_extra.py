import json
import sqlite3
import config
from pprint import pprint

CONN = sqlite3.connect(config.SQLITE_DATABASE_URI, check_same_thread=False)
CONN.row_factory = sqlite3.Row


def create_project_info_table():
    """create a table into sqlite DB of project info, which is more precise than pandas auto loading."""

    cursor = CONN.cursor()
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

    CONN.commit()


def create_part_info_table():
    """create a table into sqlite DB of project info, which is more precise than pandas auto loading."""

    cursor = CONN.cursor()
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

    CONN.commit()


def project_info_save_or_update(project_multidict):
    """save project info into Project INFO table"""

    # TODO: check project id is not null and legit
    # TODO: think about the date/real/integer type risk/problem?
    # add index to volume list

    cursor = CONN.cursor()

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

    CONN.commit()

    return 1


def project_info_delete(project):
    """delete project info/project volume/part info related to certain project"""

    cursor = CONN.cursor()
    context = (project,)
    cursor.execute("DELETE FROM project_info WHERE project=(?)", context)
    cursor.execute("DELETE FROM project_volume WHERE project=(?)", context)
    cursor.execute("DELETE FROM part_info WHERE project=(?)", context)

    CONN.commit()

    return f"project: {project} deleted"


def project_info_get(project):
    """get project info for project_info pages"""

    print("[get project-info]: ", project)
    cursor = CONN.cursor()
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
