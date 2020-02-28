from app.models import sql_query, csv_builder, load_excel
from app.views import file_builder

from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from config import TEMPLATE_FOLDER, UPLOAD_FOLDER, UPLOAD_FILE_LIST, SECRET_KEY
from werkzeug.utils import secure_filename

import json
import os

app = Flask(__name__.split('.')[0])
app.secret_key = SECRET_KEY
CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory("./static", "index.html")


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


@app.route('/project/new/info', methods=['POST'])
def save_project_info():
    result = sql_query.save_project_info(request.args)
    print("[save project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['delete'])
def delete_project_info(project):
    result = sql_query.delete_project_info(project)
    print("[delete project_info] ", result)
    return {"result": result}


@app.route('/project/<project>/info', methods=['GET'])
def get_project_info(project):
    print("[get project_info] dict find: ", sql_query.get_project_info_dict(project))
    return sql_query.get_project_info_dict(project)


@app.route('/reports/<report_name>', methods=['GET'])
def get_project_report(report_name):
    """return json as content, not attachment."""
    csv_builder.build_csv(report_name)
    # output_file_name = "report.csv"
    with open(os.path.join(TEMPLATE_FOLDER, "report.json")) as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/downloads/<path:filename>')
def download_file(filename):
    """special route for file download as attachment"""
    # maybe this works on my SUSE server...not in mac anyway
    # @after_this_request
    # def remove_file(response):
    #     os.remove(os.path.join(DOWNLOAD_FOLDER, filename))
    return send_from_directory("./downloads", filename, as_attachment=True)
