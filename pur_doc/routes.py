'''main module. Handle url with bottle framework'''
from bottle import get, post, route, run, request, view, static_file

from pur_doc.constant import FILES, TEMPLATE_PATH, DATA_PATH
from pur_doc.load_excel import load_excel
from pur_doc import xls_inject, sql, word


# return a page for file upload
@route('/upload')
@view('upload.html', template_lookup=[TEMPLATE_PATH])
def upload():
    return {}


# handle file upload request
@route('/upload', method='POST')
def save_upload():
    upload = request.files.get('upload')  # pylint: disable=no-member
    filename = upload.filename

    # save the file with correct name only
    if filename in FILES:

        # Just overwrite the file with same name
        save_path = DATA_PATH
        upload.save(save_path, overwrite=True)

        # after excel file is uploaded, trigger the event to refresh database
        load_excel(filename)

        return filename + ' updated.'

    else:
        return "wrong file uploaded"


# return the page for NL download
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

    result = {}
    result['part_list'] = part_list
    result['project'] = project
    result['vendor'] = vendor

    return result

@post('/nl/parts')
def nomination_generate():
    ''' return docx file according to form request'''
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_part_list_by_project_vendor(project, vendor)

    inject_data = sql.assemble_nl_info(project, vendor, selected_part_list)

    word.generate_nl(inject_data)

    return static_file('nl_output.docx', root='./output/')


@get('/re')
@view('risk_eval.html', template_lookup=[TEMPLATE_PATH])
def risk_eval_get():
    return {}


@post('/re')
def risk_eval_post():
    '''return risk eval xlsx file'''

    project = request.forms.get('project')
    xls_inject.xls_inject_risk_eval(project)

    return static_file('risk_eval_output.xlsx', root='./output/')
    

@get('/ss')
@view('supplier_selection.html', template_lookup=[TEMPLATE_PATH])
def supplier_selection_get():
    return {}


@post('/ss')
def supplier_selection_post():
    '''return supplier selection xlsx file'''

    project = request.forms.get('project')
    xls_inject.xls_inject_supplier_selection(project)

    return static_file('ss.zip', root='./output/')