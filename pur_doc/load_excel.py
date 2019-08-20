import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from pur_doc.constant import DB_URL, DATA_PATH

import sqlite3

CONN = sqlite3.connect(DB_URL)

# xls_name = 'nr_collector.xlsx'


def load_excel(filename):
    path_to_xls = DATA_PATH + filename

    # read the excel file to dataframe
    with pd.ExcelFile(path_to_xls) as xls:
        # loop through each sheet
        for sheet in xls.sheet_names:
            # read the sheet data
            df = pd.read_excel(xls, sheet)
            # export to sql
            df.to_sql(sheet, con=CONN, if_exists='replace', index=False)

