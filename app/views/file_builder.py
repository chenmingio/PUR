from app.views import docx_inject, xlsx_inject
from app.models import sql_nrm
from config import DOWNLOAD_FOLDER
import os
import csv

log_filename = os.path.join(DOWNLOAD_FOLDER, 'logging.csv')


def log_into_csv(filename, project, vendor, part_list):
    with open(log_filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([f'[download file]: type={filename}, project={project}, vendor={vendor}, parts={part_list}'])


def build_file(filename, project, vendor, part_list):
    log_into_csv(filename, project, vendor, part_list)
    if filename == "nomination letter":
        if bool(part_list) is False:
            part_list = sql_nrm.get_part_list_by_project_vendor(project, vendor)
        output_filename = docx_inject.generate_nl(project, vendor, part_list)
    elif filename == "cost breakdown":
        if bool(part_list) is False:
            part_list = sql_nrm.get_part_list_by_project(project)
        output_filename = xlsx_inject.xls_inject_cbd_project(project, part_list)
    elif filename == "supplier selection":
        if bool(part_list) is False:
            part_list = sql_nrm.get_part_list_by_project(project)
        output_filename = xlsx_inject.xls_inject_ss_project(project, part_list)
    elif filename == "risk evaluation":
        if bool(part_list) is False:
            part_list = sql_nrm.get_part_list_by_project(project)
        output_filename = xlsx_inject.xls_inject_risk_eval(project, part_list)
    else:
        output_filename = None

    return output_filename
