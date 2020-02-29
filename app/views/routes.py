from app.models import sql_query, csv_builder, load_excel, sql_quick_search
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


# All with API communication
# upload excel
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "'No file part'"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and (file.filename in UPLOAD_FILE_LIST):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            load_excel.load_excel(file_path)
            return f'file upload success: {filename}'


# Sourcing Document helper
@app.route('/project/<project>/vendors')
def return_vendors_by_project(project):
    vendors = sql_query.get_vendor_list_by_project(project)
    return jsonify(vendors)


@app.route('/project/<project>/vendor/<vendor>/parts')
def return_parts_by_project_vendor(project, vendor):
    parts = sql_query.get_part_list_by_project_vendor(project, vendor)
    return jsonify(parts)


@app.route('/project/<project>/parts')
def return_parts_by_project(project):
    parts = sql_query.get_part_list_by_project(project)
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
    print("[send_file] file ready to send: ", output_filename)

    if output_filename:
        return jsonify(output_filename)


# Project Info Page
@app.route('/project/new/info', methods=['POST'])
def project_info_save_or_update():
    result = sql_query.project_info_save_or_update(request.args)
    print("[save project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['delete'])
def project_info_delete(project):
    result = sql_query.project_info_delete(project)
    print("[delete project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['GET'])
def project_info_get(project):
    print("[get project_info] dict find: ", sql_query.project_info_get(project))
    return sql_query.project_info_get(project)


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
    # maybe this works on my SUSE server...not in mac anyway
    # @after_this_request
    # def remove_file(response):
    #     os.remove(os.path.join(DOWNLOAD_FOLDER, filename))
    return send_from_directory("./downloads", filename, as_attachment=True)


# Quick Search
@app.route('/qs', methods=['GET'])
def quick_search_project():
    category = request.args.get("category")
    keyword = request.args.get("keyword")

    if category == 'Project ID':
        rc = sql_quick_search.search_project_full_info_by_project(keyword)
        return jsonify(rc)
    elif category == 'Vendor ID':
        rc = sql_quick_search.search_vendor_full_info_by_vendor(keyword)
        return jsonify(rc)
    elif category == 'Project Name':
        return jsonify(sql_quick_search.wild_search_project_by_name(keyword))
    elif category == 'Vendor Name':
        rc = sql_quick_search.wild_search_vendor_by_name(keyword)
        return jsonify(rc)
    elif category == 'Part Number':
        rc = sql_quick_search.search_part_info_by_part(keyword)
        return jsonify(rc)
    else:
        # TODO consider rc is None case
        return jsonify({'fields': ["Result Not Found"], 'rows': []})
