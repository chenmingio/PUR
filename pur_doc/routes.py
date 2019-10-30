'''main module. Handle url with bottle framework'''
from bottle import get, post, route, run, request, view, static_file

from pur_doc.constant import FILES, TEMPLATE_PATH, DATA_PATH
from pur_doc.load_excel import load_excel
from pur_doc import xls_inject, sql, word

# logging setup

import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)

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
    upload = request.files.get('upload')  # pylint: disable=no-member
    filename = upload.filename

    logger.info('%s requested to upload', filename)

    # save the file with correct name only
    if filename in FILES:

        # Just overwrite the file with same name
        save_path = DATA_PATH
        upload.save(save_path, overwrite=True)

        logger.info('%s upload success', filename)

        # after excel file is uploaded, trigger the event to refresh database
        if 'xlsx' in filename:
            load_excel(filename)

        return filename + ' updated.'

    else:
        return "wrong file uploaded"



# return the page for NL download
@get('/sb')
@view('sb.html', template_lookup=[TEMPLATE_PATH])
def sb_form():
    return {}

@post('/sb')
@view('sb_parts.html', template_lookup=[TEMPLATE_PATH])
def sb_parts_form():
    project = request.forms.get('project') 

    part_list = sql.get_project_part_list(project)

    result = {}
    result['part_list'] = part_list
    result['project'] = project

    return result

@post('/sb/parts')
def sb_generate():
    ''' return xlsx file according to form request'''
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_project_part_list(project)

    xls_inject.xls_inject_sb(project, selected_part_list)

    return static_file('source_ge_output.xlsx', root='./output/')



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

    logger.info('normination letter requested for project %s w/ parts %s', project, str(part_list))
    logger.info('normination letter generated for project %s w/ parts %s', project, str(part_list))

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

    result = {}
    result['part_list'] = part_list
    result['project'] = project
    result['vendor'] = vendor

    return result

@post('/nl_pcb/parts')
def nomination_pcb_generate():
    ''' return docx file according to form request'''
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
    '''return parts for selection'''
    project = request.forms.get('project') 

    part_list = sql.get_project_part_list(project)

    result = {}
    result['part_list'] = part_list
    result['project'] = project

    return result

@post('/re/parts')
def risk_eval_generation():
    ''' return risk evaluation file according to form request'''
    selected_part_list = request.forms.getall('parts')
    project = request.forms.get('project')

    if 'all' in selected_part_list:
        selected_part_list = sql.get_project_part_list(project)
    
    logger.info('Risk Eval requested for project %s w/ parts %s', project, str(selected_part_list))
    
    xls_inject.xls_inject_risk_eval(project, selected_part_list)

    logger.info('Risk Eval generated for project %s w/ parts %s', project, str(selected_part_list))

    return static_file('risk_eval_output.xlsx', root='./output/')
    

@get('/ss')
@view('supplier_selection.html', template_lookup=[TEMPLATE_PATH])
def supplier_selection_get():
    return {}


@post('/ss')
def supplier_selection_post():
    '''return supplier selection xlsx file'''

    project = request.forms.get('project')

    logger.info('Supplier Selection requested for project %s', project)

    xls_inject.xls_inject_supplier_selection(project)

    logger.info('Supplier Selection generated for project %s', project)

    return static_file('ss.zip', root='./output/')


@get('/cbd')
@view('cbd.html', template_lookup=[TEMPLATE_PATH])
def cbd_get():
    '''get cbd start page'''
    return {}


@post('/cbd')
def cbd_post():
    '''return cbd xlsx file zip'''

    project = request.forms.get('project')

    logger.info('CBD requested for project %s', project)

    xls_inject.xls_inject_cbd(project)

    logger.info('CBD generated for project %s', project)

    return static_file('cbd.zip', root='./output/')