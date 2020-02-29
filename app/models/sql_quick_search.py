"""build dict by sql query and factory"""
import sqlite3
from collections import defaultdict
from pprint import pprint
import json

import config

conn = sqlite3.connect(config.SQLITE_DATABASE_URI, check_same_thread=False)


# conn.row_factory = sqlite3.Row


def wild_search_project_by_name(keyword):
    cursor = conn.cursor()
    sql_keyword = f'%{keyword}%'
    context = (sql_keyword, sql_keyword)
    cursor.execute("""SELECT DISTINCT project_name, project FROM (
SELECT DISTINCT project, project_name FROM project_data WHERE project_name LIKE ? UNION
SELECT DISTINCT project, project_name FROM project_info WHERE project_name LIKE ? )""", context)
    rows = cursor.fetchall()
    table_fields = ['Project Name', 'Project ID']
    table_rows = [row for row in rows]
    return dict(fields=table_fields, rows=table_rows)


def wild_search_vendor_by_name(keyword):
    cursor = conn.cursor()
    sql_keyword = f'%{keyword}%'
    context = (sql_keyword,)
    cursor.execute("""SELECT DISTINCT vendor_name, vendor FROM vendor_contact WHERE vendor_name LIKE ?""", context)
    rows = cursor.fetchall()
    table_fields = ['Vendor Name', 'Vendor ID']
    table_rows = [row for row in rows]
    return dict(fields=table_fields, rows=table_rows)


def transpose_single_row(cursor):
    """transpose one line result from sql row to field-value list"""
    row = cursor.fetchone()

    table_fields = ['Field', 'Value']
    field_list = [field_tuple[0] for field_tuple in cursor.description]  # used as row data of "Field"
    value_list = row or [None for _ in field_list]  # used as row data of "Value"
    print(f"value_list: ", value_list)
    row_tuple_list = []
    for field, value in zip(field_list, value_list):
        row_tuple_list.append((field, value))

    return dict(fields=table_fields, rows=row_tuple_list)


def search_project_full_info_by_project(project):
    cursor = conn.cursor()
    context = (project,)
    cursor.execute(
        """SELECT * FROM project_data LEFT JOIN project_info USING (project)
            LEFT JOIN plant USING (plant) WHERE project=?""", context)
    rc = transpose_single_row(cursor)
    return rc


def search_vendor_full_info_by_vendor(vendor):
    cursor = conn.cursor()
    context = (vendor,)
    cursor.execute(
        """SELECT * FROM
    vendor_contact AS VC
    LEFT JOIN vendor_basic AS VB ON VC.vendor=VB.vendor
    LEFT JOIN contract AS C ON VC.vendor=C.vendor
    LEFT JOIN quality AS Q ON VC.vendor=Q.vendor
    LEFT JOIN vendor_production AS P on VC.vendor=P.vendor
    WHERE VC.vendor=?""", context)

    rc = transpose_single_row(cursor)
    return rc


def search_part_info_by_part(part):
    cursor = conn.cursor()
    context = (part,)
    cursor.execute(
        """SELECT DISTINCT * FROM part_data AS pd
                LEFT JOIN mgm USING(mtl_group)
                LEFT JOIN mgs_sqe USING(mtl_group)
                LEFT JOIN plant USING(plant)
                WHERE pd.part=?""", context)
    rc = transpose_single_row(cursor)
    return rc
