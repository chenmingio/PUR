import app.models.sql_project_info_extra
from app.models import sql_nrm, csv_builder, load_excel, sql_quick_search, sql_logistics, logisitcs
from app.views import file_builder

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from config import TEMPLATE_FOLDER, UPLOAD_FOLDER, UPLOAD_FILE_LIST, SECRET_KEY
from werkzeug.utils import secure_filename

import json
import os

app = Flask(__name__.split('.')[0])
app.secret_key = SECRET_KEY
CORS(app)


# upload excel
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "'No file part'"
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and (file.filename.split('.')[0] in UPLOAD_FILE_LIST):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            load_excel.load_excel(file_path)
            return f'file upload success: {filename}'
        else:
            return f'file {secure_filename(file.filename)} not allowed to upload.'

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# All with API communication
# Sourcing Document helper: provide vendor options for project
@app.route('/project/<project>/vendors')
def return_vendors_by_project(project):
    vendors = sql_nrm.get_vendor_list_by_project(project)
    return jsonify(vendors)


@app.route('/project/<project>/vendor/<vendor>/parts')
def return_parts_by_project_vendor(project, vendor):
    parts = sql_nrm.get_part_list_by_project_vendor(project, vendor)
    return jsonify(parts)


@app.route('/project/<project>/parts')
def return_parts_by_project(project):
    parts = sql_nrm.get_part_list_by_project(project)
    return jsonify(parts)


# Sourcing Document
@app.route('/docs', methods=['GET'])
def return_sourcing_document():
    request_dict = request.args
    filename = request_dict.get("file")
    project = request_dict.get("project")
    vendor = request_dict.get("vendor")
    part_list = request_dict.getlist("part_list[]")

    output_filename = file_builder.build_file(filename, project, vendor, part_list)

    if output_filename:
        return jsonify(output_filename)
    else:
        return jsonify("generate file failed")


# Project Info Page
@app.route('/project/new/info', methods=['POST'])
def project_info_save_or_update():
    result = app.models.sql_project_info_extra.project_info_save_or_update(request.args)
    print("[save project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['delete'])
def project_info_delete(project):
    result = app.models.sql_project_info_extra.project_info_delete(project)
    print("[delete project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['GET'])
def project_info_get(project):
    print("[get project_info] dict find: ", app.models.sql_project_info_extra.project_info_get(project))
    return app.models.sql_project_info_extra.project_info_get(project)


# Project Report Page #TODO rethink the logic and update function
@app.route('/reports/<report_name>', methods=['GET'])
def project_report_get(report_name):
    csv_builder.build_csv(report_name)
    # output_file_name = "report.csv"
    with open(os.path.join(TEMPLATE_FOLDER, "report.json")) as f:
        data = json.load(f)

    return jsonify(data)


# Download everything from Downloads file as far as you have a name
@app.route('/downloads/<path:filename>')
def download_file(filename):
    """special route for file download as attachment"""
    return send_from_directory("./downloads", filename, as_attachment=True, cache_timeout=-1)


# Quick Search
@app.route('/qs', methods=['GET'])
def quick_search_project():
    category = request.args.get("category")
    keyword = request.args.get("keyword")

    if category == 'Project':
        if '.' in keyword:
            return jsonify(sql_quick_search.search_project_full_info_by_project(keyword))
        else:
            return jsonify(sql_quick_search.wild_search_project_by_name(keyword))
    elif category == 'Vendor':
        if keyword.isdigit():
            return jsonify(sql_quick_search.search_vendor_full_info_by_vendor(keyword))
        else:
            return jsonify(sql_quick_search.wild_search_vendor_by_name(keyword))
    else:
        return jsonify({'fields': ["Result Not Found"], 'rows': []})


# Tool Database
@app.route('/logistics/part/<part>/vendors')
def tool_database_get_vendors(part):
    if part and len(part) > 9:
        vendors = sql_logistics.get_vendor_list_from_weekly_demand(part)
        return jsonify(vendors)
    else:
        return jsonify(['wrong format'])


# Tool Database
@app.route('/logistics/part/<part>/vendor/<vendor>/tools')
def tool_database_get_tools(part, vendor):
    if part and vendor and len(part) > 9 and len(vendor) > 7:
        rc = sql_logistics.get_tool_list_by_part_and_vendor(part, vendor)
        return jsonify(rc)
    else:
        return jsonify(['wrong format'])


# Tool Database: return NRM based on part
@app.route('/logistics/part/<part>/nrm_info')
def get_nrm_part_info(part):
    target_part = logisitcs.Part(part, 1111)
    return jsonify(target_part.get_project_dict_list_from_nrm())


# Return capacity and SA for chart render
@app.route('/logistics/part/<part>/vendor/<vendor>/capacity')
def get_part_vendor_capacity_sa(part, vendor):
    target_part = logisitcs.Part(part, 1111)
    return jsonify(target_part.get_delivery(vendor))
