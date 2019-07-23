'''use dict to inject data into excel'''
from openpyxl import load_workbook


def xls_inject(workbook, sheet, inject_data, inject_map):
    # determine workbook name
    wb = load_workbook(workbook)

    # determine sheet name
    sheet = wb[sheet]

    # excute the injection
    for cell in inject_map:

        # return the key for data fetching
        data_key = inject_map[cell]

        # get the value to inject
        result = inject_data[data_key]

        # change sheet location (cell) to result 
        sheet[cell] = result

    # saving the resul to a new file xxx_output
    wb.save('risk_eval_output.xlsx')

