'''main module. Handle url with bottle framework'''
import bottle
from bottle import get, post, route, run, request, view, static_file

from db import search_part_combine, clear_data, load_data
from word import generate_nl


# return a page for file upload
@route('/upload')
@view('upload.html', template_lookup=['templates'])
def index():
    '''index'''
    return {'title': "hello"}


# url for handle file upload.
@route('/upload', method='POST')
def do_upload():
    '''Just overwrite the file with same name'''
    # forms_dict = request.forms.get
    # print(forms_dict)
    upload = request.files.get('upload')  # pylint: disable=no-member
    filename = upload.filename

    save_path = "./"
    upload.save(save_path, overwrite=True)

    if filename == "00_Collector.xlsx":
        clear_data()
        load_data(filename)

    return filename + ' updated.'


@get('/nl')
@view('nl.html', template_lookup=['templates'])
def nl_form():
    '''return a form to generate nl'''
    return {'key': 'val'}


@post('/nl')
def nomination_letter():
    ''' return docx file according to form request'''
    project = request.forms.get('project')  # pylint: disable=no-member
    vendor = request.forms.get('vendor')  # pylint: disable=no-member

    context = search_part_combine(project, vendor)
    generate_nl(context)

    return static_file('NL_g.docx', root='./')
    # return "{}, {}".format(project, vendor)


if __name__ == "__main__":
    # run(host='localhost', port=8080)
    run(server='paste', host='10.99.40.253', port=80,
        debug=True, reloader=True)

app = bottle.default_app()  # pylint: disable=invalid-name
