from app.views import docx_inject, xlsx_inject
from app.models import sql_query


def build_file(filename, project, vendor, part_list):
    if filename == "nomination letter":
        if "all" in part_list:
            part_list = sql_query.get_part_list_by_project_vendor(project, vendor)
        output_filename = docx_inject.generate_nl(project, vendor, part_list)
    elif filename == "CBD":
        output_filename = xlsx_inject.xls_inject_cbd_project(project)
    elif filename == "supplier selection":
        output_filename = xlsx_inject.xls_inject_ss_project(project)
    elif filename == "risk evaluation":
        if "all" in part_list:
            part_list = sql_query.get_part_list_by_project(project)
        output_filename = xlsx_inject.xls_inject_risk_eval(project, part_list)
    else:
        output_filename = None

    return output_filename
