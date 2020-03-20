"""build dict by sql query and factory"""
from datetime import date
import sqlite3
from config import CAPACITY_BUFF, SQLITE_DATABASE_URI
from app.models.sql_NRM import get_vendor_weeks_per_year

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


def get_weekly_max_capacity_by_date(part, vendor, date):
    year = (date.year - 1) if date.month < 6 else date.year
    print("year: ", year)
    cursor = conn.cursor()
    context = (part, vendor, year)
    cursor.execute("""SELECT SUM(volume * quota /100) AS year_volume 
            FROM nomi_part AS NP LEFT JOIN rfq_part AS RP USING (project, part, year) 
            WHERE volume>0 AND quota>0 AND part=? AND vendor=? AND year=?""", context)
    row = cursor.fetchone()
    year_volume = row[0]
    wpy = get_vendor_weeks_per_year(vendor)
    if year_volume:
        print(f">>>[debug]: year vol: {year_volume}, wpy: {wpy}")
        return year_volume / wpy * 1.3


def get_delivery(part, vendor):
    cursor = conn.cursor()
    context = (part, vendor)
    cursor.execute("""SELECT DATE(start_of_week) AS date, to_deliver_qty_week AS qty FROM weekly_demand 
    WHERE trim(part)=? AND vendor=? ORDER BY DATE""", context)
    rows = cursor.fetchall()
    demand = {'date': [row[0] for row in rows], 'qty': [row[1] / 1000 for row in rows]}
    if rows:
        capacity_tuples = []

        delivery_start = date.fromisoformat(rows[0][0])
        delivery_end = date.fromisoformat(rows[-1][0])
        intervals = [(date(year, 6, 1), date(year + 1, 5, 31)) for year in
                     range(delivery_start.year - 1, delivery_end.year + 1)]

        print(">>> interval is: ", intervals)
        for date_0, date_1 in intervals:
            if delivery_start > date_1 or delivery_end < date_0:
                pass
            else:
                capacity_start = max(date_0, delivery_start)
                capacity_end = min(date_1, delivery_end)
                _capacity = get_weekly_max_capacity_by_date(part, vendor, capacity_start)
                weekly_capacity = _capacity / 1000 if _capacity else []
                capacity_tuples.append(
                    {'interval': {'begin': capacity_start.isoformat()[:11], 'end': capacity_end.isoformat()[:11]},
                     'capacity': weekly_capacity})
                # TODO python dict is slow hmmm? use list as api and parse back to object in front end?

        return {'demand': demand, 'capacities': capacity_tuples}
