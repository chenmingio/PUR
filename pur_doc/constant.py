# store the constant

# path management
DB_URL = './pur_doc/data/nr.db'

TEMPLATE_PATH = "./pur_doc/templates/"

DATA_PATH = "./pur_doc/data/"

FILE_PATH = "./pur_doc/output"


# excel files names

FILES = ['01_nr.xlsx', '02_vendor.xlsx', '03_project.xlsx', '04_constant.xlsx' , 'nl.docx']

XLS_FILES = ['nr_collector', 'vendor_data', 'project_data']

NR_SHEETS = ['project_data', 'part_data', 'project_timing', 'sourcing_concept', 'rfq_part', 'rfq_invest', 'nomi_part', 'nomi_invest']

VENDOR_SHEETS = []

PROJECT_SHEETS = []

# FY exchange rate to CNY

EX_RATE = {'EUR': 8.14, 'CNY': 1, 'USD': 6.898}

# PVO threshold

LOCAL_SB_THRESHOLD = 250 # temprory reduced

# CBD Summery Sheet Password
cbd_sheet_password = '800520'