'''use dict to inject data into excel'''
from openpyxl import load_workbook
from pur_doc import sql

get_data = sql.assemble_project


def deep_dict(dict, key_chain):

    while True:

        # make sure val is dict. then can go deeper. otherwise return val.
        if (type(dict) == str) or (dict is None) or (len(key_chain) == 0):
            return dict
        else:
        # if next level available, apply deep_dict function to next level
            next_dict = dict.get(key_chain[0])
            key_chain.pop(0)

            deep_dict(next_dict, key_chain)

def xls_inject(inject_book, project):
    '''xxx'''

    # load the inject book you need
    workbook = inject_book['workbook']
    sheet = inject_book['sheet']
    inject_map = inject_book['inject_map']

    if 'sourcing_ge' in workbook:
        inject_data = get_data(project, sb=True)
    else:
        inject_data = get_data(project)


    # load workbook into openpyxl
    wb = load_workbook(workbook)

    # load the sheet
    sheet = wb[sheet]

    # excute the injection
    for cell in inject_map:

        # return the key for data fetching
        key_chain = inject_map[cell].split('.')


        # get the value to inject
        value = deep_dict(inject_data, key_chain)
        print(value)


        # change sheet location (cell) to result 
        sheet[cell] = value

    # saving the resul to a new file xxx_output
    wb.save(workbook + '_output.xlsx')

