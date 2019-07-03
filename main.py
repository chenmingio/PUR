from bottle import get, post, route, run, request, view, static_file

from db import search_part_combine
from word import generate_nl


# return a page for file upload
@route('/')
@view('upload.html', template_lookup=['templates'])
def index():
    '''index'''
    return {'title': "hello"}


# url for handle file upload
@route('/upload', method='POST')
def do_upload():
    '''upoload page'''
    upload = request.files.get('upload')

    save_path = "./"
    upload.save(save_path, overwrite=True)
    return 'OK'


@get('/nl')
@view('nl.html', template_lookup=['templates'])
def nl_form():
    '''return a form to generate nl'''
    return {'key': 'val'}


@post('/nl')
def nomination_letter():
    ''' return docx file according to form request'''
    project = request.forms.get('project')
    vendor = request.forms.get('vendor')

    context = search_part_combine(project, vendor)
    generate_nl(context)

    return static_file('NL_g.docx', root='./')
    # return "{}, {}".format(project, vendor)


if __name__ == "__main__":
    run(server='paste', host='10.99.40.253', port=80,
        debug=True, reloader=True)

# app = bottle.default_app()
