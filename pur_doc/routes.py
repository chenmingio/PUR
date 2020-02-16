from bottle import get, post, route, run, request, static_file
from bottle import jinja2_view as view
from pur_doc.constant import FILES, TEMPLATE_PATH, DATA_PATH
from pur_doc.load_excel import load_excel
from pur_doc import xls_inject, sql, word


# return index
@route('/')
@view('index.html', template_lookup=[TEMPLATE_PATH])
def index():
    return {}


# return a page for file upload
@route('/upload')
@view('upload.html', template_lookup=[TEMPLATE_PATH])
def upload():
    return {}


# handle file upload request
@route('/upload', method='POST')
def save_upload():
    upload = request.files.get('upload')
    filename = upload.filename

    # save the file with correct name only
    if filename in FILES:

        # Just overwrite the file with same name
        save_path = DATA_PATH
        upload.save(save_path, overwrite=True)

        # after excel file is uploaded, trigger the event to refresh database
        if 'xlsx' in filename:
            load_excel(filename)

        return filename + ' updated.'

    else:
        return "wrong file uploaded"


@get('/sb')
@view('sb.html', template_lookup=[TEMPLATE_PATH])
def sb_form():
    return {}


@post('/sb')
@view('sb_parts.html', template_lookup=[TEMPLATE_PATH])
def sb_parts_form():
    project = request.forms.get('project')
    part_list = sql.get_project_part_list(project)

    result = {'part_list': part_list, 'project': project}

    return result


@post('/sb/parts')
def sb_generate():
    """ return xlsx file according to form request"""

    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_project_part_list(project)

    xls_inject.xls_inject_sb(project, selected_part_list)

    return static_file('source_ge_output.xlsx', root='./output/')



@get('/nl')
@view('nl.html', template_lookup=[TEMPLATE_PATH])
def nl_form():
    return {}


@post('/nl')
@view('nl_parts.html', template_lookup=[TEMPLATE_PATH])
def nl_parts_form():
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    part_list = sql.get_part_list_by_project_vendor(project, vendor)

    result = {'part_list': part_list, 'project': project, 'vendor': vendor}

    return result


@post('/nl/parts')
def nomination_generate():
    """ return docx file according to form request"""
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_part_list_by_project_vendor(project, vendor)

    word.generate_nl(project, vendor, selected_part_list)
    return static_file('nl_output.docx', root='./output/')


# return the page for PCB NL download
@get('/nl_pcb')
@view('nl_pcb.html', template_lookup=[TEMPLATE_PATH])
def nl_pcb_form():
    return {}


@post('/nl_pcb')
@view('nl_pcb_parts.html', template_lookup=[TEMPLATE_PATH])
def nl_pcb_parts_form():
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    part_list = sql.get_part_list_by_project_vendor(project, vendor)

    result = {'part_list': part_list, 'project': project, 'vendor': vendor}

    return result


@post('/nl_pcb/parts')
def nomination_pcb_generate():
    """ return docx file according to form request"""
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_part_list_by_project_vendor(project, vendor)

    inject_data = sql.assemble_nl_info(project, vendor, selected_part_list)

    word.generate_nl_pcb(inject_data)

    return static_file('nl_pcb_output.docx', root='./output/')


@get('/re')
@view('re.html', template_lookup=[TEMPLATE_PATH])
def risk_eval_get():
    return {}


@post('/re')
@view('re_parts.html', template_lookup=[TEMPLATE_PATH])
def risk_eval_parts():
    """return parts for selection"""
    project = request.forms.get('project')

    part_list = sql.get_part_list_by_project(project)

    result = {'part_list': part_list, 'project': project}

    return result


@post('/re/parts')
def risk_eval_generation():
    """ return risk evaluation file according to form request"""
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_part_list_by_project(project)

    xls_inject.xls_inject_risk_eval(project, selected_part_list)

    return static_file('risk_eval_output.xlsx', root='./output/')


@get('/ss')
@view('ss.html', template_lookup=[TEMPLATE_PATH])
def supplier_selection_form():
    return {}


@post('/ss')
def supplier_selection_return():
    """return supplier selection xlsx file"""

    project = request.forms.get('project')
    xls_inject.xls_inject_ss_project(project)

    return static_file('supplier_selection.zip', root='./output/')


@get('/cbd')
@view('cbd.html', template_lookup=[TEMPLATE_PATH])
def cbd_get():
    """get cbd start page"""
    return {}


@post('/cbd')
def cbd_post():
    """return cbd xlsx file zip"""

    project = request.forms.get('project')

    xls_inject.xls_inject_cbd_project(project)

    return static_file('cbd.zip', root='./output/')
