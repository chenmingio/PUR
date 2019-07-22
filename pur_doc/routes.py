'''main module. Handle url with bottle framework'''
from bottle import get, post, route, run, request, view, static_file

from pur_doc.constant import FILES, TEMPLATE_PATH, FILE_PATH
from pur_doc.load_excel import load_excel


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
        save_path = FILE_PATH
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
def nomination_letter():
    ''' return docx file according to form request'''
    project = request.forms.get('project')  # pylint: disable=no-member
    vendor = request.forms.get('vendor')  # pylint: disable=no-member

    context = search_part_combine(project, vendor)
    generate_nl(context)

    return static_file('NL_g.docx', root='./')
    # return "{}, {}".format(project, vendor)

