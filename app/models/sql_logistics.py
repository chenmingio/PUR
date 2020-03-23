"""build dict by sql query and factory"""
from datetime import date
import sqlite3
from config import CAPACITY_BUFF, SQLITE_DATABASE_URI
from app.models.sql_nrm import get_vendor_weeks_per_year

conn = sqlite3.connect(SQLITE_DATABASE_URI, check_same_thread=False)


def get_vendor_list_from_nrm_by_part(part):
    cursor = conn.cursor()
    context = (part, part[:3] + part[4:7] + part[8:])
    cursor.execute(
        """SELECT DISTINCT vendor FROM (
            SELECT DISTINCT vendor FROM nomi_part WHERE trim(part)=? UNION
            SELECT DISTINCT cast(supplier as text) FROM tool_database WHERE part=?)""", context)
    rows = cursor.fetchall()
    return [item[0] for item in rows]


def get_vendor_list_from_weekly_demand(part):
    cursor = conn.cursor()
    context = (part,)
    cursor.execute(
        """SELECT DISTINCT vendor FROM weekly_demand WHERE trim(part)=?""", context)
    rows = cursor.fetchall()
    if rows:
        return [item[0] for item in rows]


def get_tool_list_by_part_and_vendor(part, vendor):
    cursor = conn.cursor()
    context = (part[:3] + part[4:7] + part[8:], vendor)
    cursor.execute(
        """SELECT DISTINCT tool FROM tool_database WHERE part=? AND supplier=?""", context)
    rows = cursor.fetchall()
    return [item[0] for item in rows]


def build_volumes_object_for_nrm_vendor(project, part, vendor):
    cursor = conn.cursor()
    context = (project, part, vendor)
    cursor.execute("""SELECT year, volume * quota /100 AS volume 
        FROM nomi_part AS NP LEFT JOIN rfq_part AS RP USING (project, part, year) 
        WHERE volume>0 AND quota>0 AND project=? AND part=? AND vendor=?""", context)
    rows = cursor.fetchall()

    wpy = get_vendor_weeks_per_year(vendor)
    rc = [{'year': row[0], 'year_volume': row[1], 'week_capacity': row[1] / wpy * CAPACITY_BUFF} for row in
          rows]
    return rc


def get_nrm_part_volume_by_vendor_and_year(part, vendor, year):
    cursor = conn.cursor()
    context = (part, vendor, year)
    cursor.execute("""SELECT SUM(volume * quota /100)/1000 AS year_volume 
                FROM nomi_part AS NP LEFT JOIN rfq_part AS RP USING (project, part, year) 
                WHERE volume>0 AND quota>0 AND part=? AND vendor=? AND year=?""", context)
    row = cursor.fetchone()
    return row[0] if row else None


def get_nl_part_volume_by_vendor_and_year(part, vendor, year):
    cursor = conn.cursor()
    context = (part, vendor, year)
    cursor.execute("""SELECT SUM(volume)/1000 as year_volume
    FROM contract_volume WHERE part=? AND vendor=? AND year=?""", context)
    row = cursor.fetchone()
    return row[0] if row else None


def get_apn_part_volume_by_vendor_and_year(part, vendor, year):
    cursor = conn.cursor()
    context = (part, vendor, year)
    cursor.execute("""SELECT SUM(capacity)/1000 as year_volume
    FROM apn_volume WHERE capacity>0 AND part=? AND vendor=? AND year=?""", context)
    row = cursor.fetchone()
    return row[0] if row else None


def get_tool_capacity_by_vendor(part, vendor, year):
    cursor = conn.cursor()
    context = (part, vendor)
    cursor.execute("""SELECT capacity/1000 FROM tool_capacity WHERE part=? AND vendor=?""", context)
    row = cursor.fetchone()
    return row[0] if row else None


def get_demand(part, vendor):
    cursor = conn.cursor()
    context = (part, vendor)
    cursor.execute("""SELECT DATE(start_of_week) AS date, to_deliver_qty_week/1000 AS qty FROM weekly_demand 
    WHERE trim(part)=? AND vendor=? ORDER BY DATE""", context)
    rows = cursor.fetchall()
    demand = {'date': [row[0] for row in rows], 'qty': [row[1] for row in rows]}
    return demand


def get_fiscal_year(date_obj):
    return date_obj.year if date_obj.month > 5 else date_obj.year - 1


def get_delivery(part, vendor):
    demand = get_demand(part, vendor)
    demand_dates = get_demand(part, vendor)['date']
    if demand_dates:

        delivery_start = date.fromisoformat(demand_dates[0])
        delivery_end = date.fromisoformat(demand_dates[-1])
        intervals = [(date(year, 6, 1), date(year + 1, 5, 31)) for year in
                     range(delivery_start.year - 1, delivery_end.year + 1)]

        capacities = dict()

        for capacity_function, key in zip(
                [get_nl_part_volume_by_vendor_and_year, get_apn_part_volume_by_vendor_and_year,
                 get_tool_capacity_by_vendor], ["nl", "apn", "tool"]):

            # each nl/apn/tool value is a list of capacity object, like [{'interval': xxx, 'capacity': number}...]
            capacities[key] = []
            for date_0, date_1 in intervals:
                if delivery_start > date_1 or delivery_end < date_0:
                    pass
                else:
                    capacity_start = max(date_0, delivery_start)
                    capacity_end = min(date_1, delivery_end)

                    rc = capacity_function(part, vendor, get_fiscal_year(capacity_start))
                    if key == "tool":  # rc is the max capacity
                        week_capacity = rc
                    else:  # rc is yearly volumes̵
                        week_capacity = rc / get_vendor_weeks_per_year(vendor) if rc else None

                    capacities[key].append(
                        {'interval': {'begin': capacity_start.isoformat()[:11], 'end': capacity_end.isoformat()[:11]},
                         'capacity': week_capacity})
                # TODO python dict is slow? use list as api and parse back to object in front end?

        return {'demand': demand, 'capacities': capacities}
