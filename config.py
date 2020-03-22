import os

SECRET_KEY = b'really hard to guess'

# path management
basedir = os.path.abspath(os.path.dirname(__file__))
DATA_FOLDER = os.path.join(basedir, 'data')
SQLITE_DATABASE_URI = os.path.join(basedir, 'data', 'nr.db')
TEMPLATE_FOLDER = os.path.join(basedir, 'app', 'templates')
DOWNLOAD_FOLDER = os.path.join(basedir, 'app', 'downloads')
UPLOAD_FOLDER = os.path.join(basedir, 'app', 'uploads')

# Upload File Whitelist

UPLOAD_FILE_LIST = [
    '01_MGM',
    '02_MGS_SQE',
    '03_Hella_Contact',
    '04_Hella_Plant',
    '05_FY_Ex_Rate',

    '11_Contract_Status',
    '12_Vendor_Rating',
    '13_Vendor_Production',
    '14_Vendor_Quality',
    '15_Vendor_Team',

    '30_vendor_collector',
    '31_nomination_roadmap_collector',
    '32_logistics_collector',
]

UPLOAD_SHEET_LIST = [

    # 00:09 Internal Constants
    'mgm',
    'mgs_sqe',
    'hella_person',
    'plant',
    'ex_rate',
    'duns',

    # 10:15 vendor info
    'contract',
    'vendor_basic',
    'vendor_team',
    'vendor_production',
    'quality',

    # 30 vendor collector
    'duns',
    'vendor_contact',


    # 31 nomination roadmap collector
    'project_data', 'part_data', 'project_timing', 'sourcing_concept',
    'rfq_part', 'rfq_invest', 'nomi_part', 'nomi_invest',

    # 32 logistics collector
    'tool_database', 'received_quantity', 'weekly_demand', 'contract_volume', 'apn_volume', 'tool_capacity',

    # future DW sheets
    'ppm',

    # templates
    'nl',
    'nl_pcb',
]

ALLOWED_EXTENSIONS = ['xlsx', 'docx',]

# Excel Sheet Password
EXCEL_PASSWORD = '800520'

# Business Constants
EX_RATE = {'EUR': 8.14, 'CNY': 1, 'USD': 6.898}
LOCAL_SB_THRESHOLD = 250  # temporary reduced
DEFAULT_WPY = 50
CAPACITY_BUFF = 1.3