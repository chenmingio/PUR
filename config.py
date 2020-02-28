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
UPLOAD_FILE_LIST = ['01_nr.xlsx', '02_vendor.xlsx', '04_constant.xlsx', 'Contract_Status.xlsx',
                    'MGS_SQE_MGM_Matrix']
UPLOAD_SHEET_LIST = ['contract',  # contract status
                     'mgm', 'mgs_sqe',  # mgx matrix
                     'project_data', 'part_data', 'project_timing', 'sourcing_concept', 'rfq_part', 'rfq_invest',
                     'nomi_part', 'nomi_invest',  # 01_nr
                     'vendor_basic', 'vendor_team', 'vendor_production', 'vendor_contact',
                     'quality', 'ppm', 'forecast',  # 02_vendor
                     'hella_person', 'duns', 'plant', 'ex_rate'  # constant
                     ]
ALLOWED_EXTENSIONS = {'xlsx', 'docx', 'db'}

# Excel Sheet Password
EXCEL_PASSWORD = '800520'

# Business Constants
EX_RATE = {'EUR': 8.14, 'CNY': 1, 'USD': 6.898}
LOCAL_SB_THRESHOLD = 250  # temporary reduced
