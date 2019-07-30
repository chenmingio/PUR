'''use dict to inject data into excel'''
import os, zipfile
from openpyxl import load_workbook
from pur_doc import sql, constant
TEMPLATE_PATH = constant.TEMPLATE_PATH

from os import remove

def xls_inject_risk_eval(project):
    '''xxx'''

    file_name = 'risk_eval'
    file_path = TEMPLATE_PATH + file_name + '.xlsx'
    sheet_name = 'Risk Evaluation'

    # load workbook into openpyxl
    wb = load_workbook(file_path)

    # load the sheet
    sheet = wb[sheet_name]

    # get the value
    project_dict = sql.assemble_project(project)

    # start injection

    sheet['E1'] = project_dict['project']['project_name'] or None

    sheet['F4'] = project_dict['parts']['part_1']['general_info']['part'] or None
    sheet['H4'] = project_dict['parts']['part_2']['general_info']['part'] or None
    sheet['J4'] = project_dict['parts']['part_3']['general_info']['part'] or None
    sheet['L4'] = project_dict['parts']['part_4']['general_info']['part'] or None
    sheet['N4'] = project_dict['parts']['part_5']['general_info']['part'] or None

    sheet['F5'] = project_dict['parts']['part_1']['general_info']['part_description'] or None
    sheet['H5'] = project_dict['parts']['part_2']['general_info']['part_description'] or None
    sheet['J5'] = project_dict['parts']['part_3']['general_info']['part_description'] or None
    sheet['L5'] = project_dict['parts']['part_4']['general_info']['part_description'] or None
    sheet['N5'] = project_dict['parts']['part_5']['general_info']['part_description'] or None

    sheet['F6'] = project_dict['parts']['part_1']['general_info']['mtl_group'] or None
    sheet['H6'] = project_dict['parts']['part_2']['general_info']['mtl_group'] or None
    sheet['J6'] = project_dict['parts']['part_3']['general_info']['mtl_group'] or None
    sheet['L6'] = project_dict['parts']['part_4']['general_info']['mtl_group'] or None
    sheet['N6'] = project_dict['parts']['part_5']['general_info']['mtl_group'] or None

    sheet['F7'] = project_dict['parts']['part_1']['general_info']['volume_avg'] or None
    sheet['H7'] = project_dict['parts']['part_2']['general_info']['volume_avg'] or None
    sheet['J7'] = project_dict['parts']['part_3']['general_info']['volume_avg'] or None
    sheet['L7'] = project_dict['parts']['part_4']['general_info']['volume_avg'] or None
    sheet['N7'] = project_dict['parts']['part_5']['general_info']['volume_avg'] or None

    sheet['F8'] = project_dict['parts']['part_1']['general_info']['target_price100_EUR'] or None
    sheet['H8'] = project_dict['parts']['part_2']['general_info']['target_price100_EUR'] or None
    sheet['J8'] = project_dict['parts']['part_3']['general_info']['target_price100_EUR'] or None
    sheet['L8'] = project_dict['parts']['part_4']['general_info']['target_price100_EUR'] or None
    sheet['N8'] = project_dict['parts']['part_5']['general_info']['target_price100_EUR'] or None

    sheet['F9'] = project_dict['parts']['part_1']['general_info']['part_life_time'] or None
    sheet['H9'] = project_dict['parts']['part_2']['general_info']['part_life_time'] or None
    sheet['J9'] = project_dict['parts']['part_3']['general_info']['part_life_time'] or None
    sheet['L9'] = project_dict['parts']['part_4']['general_info']['part_life_time'] or None
    sheet['N9'] = project_dict['parts']['part_5']['general_info']['part_life_time'] or None

    sheet['F10'] = project_dict['project']['plant'] if project_dict['parts']['part_1']['general_info']['part'] else None
    sheet['H10'] = project_dict['project']['plant'] if project_dict['parts']['part_2']['general_info']['part'] else None
    sheet['J10'] = project_dict['project']['plant'] if project_dict['parts']['part_3']['general_info']['part'] else None
    sheet['L10'] = project_dict['project']['plant'] if project_dict['parts']['part_4']['general_info']['part'] else None
    sheet['N10'] = project_dict['project']['plant'] if project_dict['parts']['part_5']['general_info']['part'] else None

    sheet['F12'] = project_dict['project']['sop_hella_date'] if project_dict['parts']['part_1']['general_info']['part'] else None
    sheet['H12'] = project_dict['project']['sop_hella_date'] if project_dict['parts']['part_2']['general_info']['part'] else None
    sheet['J12'] = project_dict['project']['sop_hella_date'] if project_dict['parts']['part_3']['general_info']['part'] else None
    sheet['L12'] = project_dict['project']['sop_hella_date'] if project_dict['parts']['part_4']['general_info']['part'] else None
    sheet['N12'] = project_dict['project']['sop_hella_date'] if project_dict['parts']['part_5']['general_info']['part'] else None

    sheet['F13'] = project_dict['parts']['part_1']['general_info']['raw_mtl'] or None
    sheet['H13'] = project_dict['parts']['part_2']['general_info']['raw_mtl'] or None
    sheet['J13'] = project_dict['parts']['part_3']['general_info']['raw_mtl'] or None
    sheet['L13'] = project_dict['parts']['part_4']['general_info']['raw_mtl'] or None
    sheet['N13'] = project_dict['parts']['part_5']['general_info']['raw_mtl'] or None

    sheet['F14'] = project_dict['parts']['part_1']['general_info']['mgm'] or None
    sheet['H14'] = project_dict['parts']['part_2']['general_info']['mgm'] or None
    sheet['J14'] = project_dict['parts']['part_3']['general_info']['mgm'] or None
    sheet['L14'] = project_dict['parts']['part_4']['general_info']['mgm'] or None
    sheet['N14'] = project_dict['parts']['part_5']['general_info']['mgm'] or None

    sheet['F15'] = project_dict['parts']['part_1']['general_info']['mgs'] or None
    sheet['H15'] = project_dict['parts']['part_2']['general_info']['mgs'] or None
    sheet['J15'] = project_dict['parts']['part_3']['general_info']['mgs'] or None
    sheet['L15'] = project_dict['parts']['part_4']['general_info']['mgs'] or None
    sheet['N15'] = project_dict['parts']['part_5']['general_info']['mgs'] or None

    sheet['F16'] = project_dict['project']['pur'] if project_dict['parts']['part_1']['general_info']['part'] else None
    sheet['H16'] = project_dict['project']['pur'] if project_dict['parts']['part_2']['general_info']['part'] else None
    sheet['J16'] = project_dict['project']['pur'] if project_dict['parts']['part_3']['general_info']['part'] else None
    sheet['L16'] = project_dict['project']['pur'] if project_dict['parts']['part_4']['general_info']['part'] else None
    sheet['N16'] = project_dict['project']['pur'] if project_dict['parts']['part_5']['general_info']['part'] else None

    # save the inject
    wb.save('./output/' + file_name + '_output.xlsx')


def xls_inject_supplier_selection(project):
    '''xxx'''

    # get the input data
    project_dict = sql.assemble_project(project)

    file_name = 'supplier_selection'
    file_path = TEMPLATE_PATH + file_name + '.xlsx'
    sheet_name = 'Supplier Selection'

    # load workbook into openpyxl
    wb = load_workbook(file_path)

    # load the sheet
    sheet = wb[sheet_name]

    part_qty = len(project_dict['project']['part_list'])
    
    output_file_list = []

    for n in range(1, part_qty +1):

        # start injection

        part_n = 'part_' + str(n)
        part = (project_dict['project']['part_list'][n - 1])

        sheet['E6'] = project_dict['project']['project_name'] or None
        sheet['K6'] = project_dict['project']['project'] or None

        sheet['E8'] = project_dict['parts'][part_n]['general_info']['part'] or None # may change to part
        sheet['K8'] = project_dict['parts'][part_n]['general_info']['part_description'] or None

        sheet['K10'] = project_dict['parts'][part_n]['general_info']['mtl_group'] or None

        sheet['E12'] = project_dict['project']['sop_hella_date'] or None
        sheet['K12'] = project_dict['parts'][part_n]['general_info']['part_life_time'] or None

        sheet['E14'] = project_dict['parts'][part_n]['general_info']['volume_avg'] or None
        sheet['K14'] = project_dict['parts'][part_n]['general_info']['pvo'] or None

        sheet['E16'] = project_dict['parts'][part_n]['general_info']['mgm'] or None
        sheet['K16'] = project_dict['parts'][part_n]['general_info']['mgs'] or None

        sheet['E18'] = project_dict['project']['pur'] or None
        sheet['K18'] = project_dict['project']['plant'] or None

        sheet['E20'] = project_dict['parts'][part_n]['general_info']['raw_mtl'] or None

        sheet['R23'] = project_dict['parts'][part_n]['general_info']['risk_level'] or None

        # TODO add planned sourcing date value into R25

        # save the inject
        outout_file_name = './output/' + file_name + '_' + part + '_output.xlsx'
        wb.save(outout_file_name)
        output_file_list.append(outout_file_name)

    # zip the output files
    with zipfile.ZipFile('./output/ss.zip', 'w') as new_zip:
        for name in output_file_list:
            new_zip.write(name)

    # remove the excel files
    for name in output_file_list:
        remove(name)


def xls_inject_sb(project):
    '''xxx'''

    # get the input data
    project_dict = sql.assemble_project(project, sb=True)

    file_name = 'test_source_ge'
    file_path = './pur_doc/templates/' + file_name + '.xlsx'
    sheet_name = 'Input'

    # load workbook into openpyxl
    wb = load_workbook(file_path)

    # load the sheet
    sheet = wb[sheet_name]

    # start the injection
    
    sheet['H3'] = project_dict['project']['project'] or None
    sheet['H4'] = project_dict['project']['project_name'] or None
    sheet['H5'] = project_dict['project']['customer'] or None
    sheet['W3'] = project_dict['project']['dd_location'] or None
    sheet['W4'] = project_dict['project']['plant'] or None
    sheet['AK3'] = project_dict['project']['pur'] or None
    sheet['AK4'] = project_dict['project']['pjm'] or None
    sheet['AK5'] = project_dict['project']['md'] or None
    sheet['AK6'] = project_dict['project']['sqa'] or None

    
    sheet['H9'] = project_dict['project']['sop_hella_date'][0:4] or None
    sheet['H10'] = project_dict['project']['year_1_volume'] or None
    sheet['L10'] = project_dict['project']['year_2_volume'] or None
    sheet['P10'] = project_dict['project']['year_3_volume'] or None
    sheet['T10'] = project_dict['project']['year_4_volume'] or None
    sheet['X10'] = project_dict['project']['year_5_volume'] or None
    sheet['AB10'] = project_dict['project']['year_6_volume'] or None
    sheet['AF10'] = project_dict['project']['year_7_volume'] or None
    sheet['AJ10'] = project_dict['project']['year_8_volume'] or None
    sheet['AN10'] = project_dict['project']['year_9_volume'] or None
    sheet['AR10'] = project_dict['project']['year_10_volume'] or None

    sheet['F16'] = int(project_dict['project']['run_rate_date']) or None 
    sheet['F17'] = project_dict['project']['pv_hella_date'][0:10] or None
    sheet['F18'] = project_dict['project']['sop_hella_date'][0:10]or None
    sheet['F19'] = project_dict['project']['sop_customer_date'][0:10] or None

    # save the inject
    wb.save(file_name + '_output.xlsx')
