import pandas as pd
import sqlite3

from config import SQLITE_DATABASE_URI, UPLOAD_SHEET_LIST

CONN = sqlite3.connect(SQLITE_DATABASE_URI, check_same_thread=False)


def load_excel(filepath):

    # read the excel file to dataframe
    with pd.ExcelFile(filepath) as xls:
        # loop through each sheet
        for sheet in xls.sheet_names:
            if sheet in UPLOAD_SHEET_LIST:
                # read the sheet data
                df = pd.read_excel(xls, sheet)
                # export to sql
                df.to_sql(sheet, con=CONN, if_exists='replace', index=False)
                print("[upload file] success: ", filepath, sheet)

# TODO: limited the allowed filename and sheet names
# TODO: pandas change date to timestamp. I don't need time. Find a way to cast into date format when load.
