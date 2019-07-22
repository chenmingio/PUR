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

WORKBOOK = './data/risk_eval.xlsx'
SHEET = 'Risk Evaluation'
INJECT_DATA = {'index': 55, 'project': '1111E.001239', 'project_name': 'APS/HKG Honda Fit', 'customer': 'TBD', 'dd_location': 'TBD', 'plant': 1111, 'pjm': 'Jeff Gu', 'pur': 'Chen Ming', 'md': 'Wang Quancheng', 'sqa': 'Daisy Dong', 'me': 'Gu Qi', 'controlling': 'Flynn Tang', 'log': 'Zack Zheng', 'sop_hella_date': '1949-10-01 00:00:00', 'sop_customer_date': '1949-10-01 00:00:00', 'run_rate_date': '1949-10-01 00:00:00', 'pv_hella_date': '1949-10-01 00:00:00', 'year_1_volume': 9999, 'year_2_volume': 9999, 'year_3_volume': 9999, 'year_4_volume': 9999, 'year_5_volume': 9999, 'year_6_volume': 9999, 'year_7_volume': 9999, 'year_8_volume': 9999, 'year_9_volume': 9999, 'year_10_volume': 9999, 'production_line': 'test_production_line', 'fg_part_number': '123456abcd', 'customer_nomination_available': 'YES', 'budget_available': 'YES'}
INJECT_MAP = {'E1': 'project_name'}

if __name__ == '__main__':
    xls_inject(WORKBOOK, SHEET, INJECT_DATA, INJECT_MAP)