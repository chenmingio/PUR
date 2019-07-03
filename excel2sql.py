import openpyxl
from openpyxl.utils import get_column_letter

import sqlite3

# connect DB
conn = sqlite3.connect('nr.db')
c = conn.cursor()


def load_data(file):

    # connect excel
    wb = openpyxl.load_workbook(file)
    sheets = wb.get_sheet_names()

    for sheet_name in sheets:

        sheet = wb.get_sheet_by_name(sheet_name)

        # read titles
        max_col = sheet.max_column
        titles = [sheet[get_column_letter(i) + '1'].value for i in range(1, max_col + 1)]

        # print(titles)

        # prepare insert_list
        insert_list = []
        max_row = sheet.max_row
        print(max_row)
        for j in range(2, max_row + 1):
            row = tuple([sheet[get_column_letter(i) + str(j)].value for i in range(1,
                max_col + 1)])
            print(row)
            insert_list.append(row)

        # print(insert_list)

        # insert list into sql
        # prepare string
        question_mark = '(' + "?," * (len(titles) - 1) + '?)'
        string = "INSERT INTO {0} VALUES {1}".format(sheet_name, question_mark)
        # print(string)

        c.executemany(string, insert_list)

    # close connection to DB
    conn.commit()
    conn.close()


if __name__=="__main__":
    load_data('00_Collector.xlsx')

