import pandas as pd
import sqlite3
import os

from config import SQLITE_DATABASE_URI, DOWNLOAD_FOLDER

CONN = sqlite3.connect(SQLITE_DATABASE_URI, check_same_thread=False)

query_dict = {
    "project_info": "SELECT * FROM part_info",
    "project_data": "SELECT * FROM part_data",
}


def build_csv(report_name):
    query_string = query_dict[report_name]
    data = pd.read_sql_query(query_string, CONN)
    data.to_csv(os.path.join(DOWNLOAD_FOLDER, "report.csv"), index=False)
