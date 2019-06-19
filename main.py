import bottle
import jinja2
import db

route = bottle.route
run = bottle.run
request = bottle.request
response = bottle.response
debug = bottle.debug
view = bottle.jinja2_view

search_part_combine = db.search_part_combine


# return a page for file upload
@route('/')
@view('upload.html', template_lookup=['templates'])
def index():
    return {'title': "hello"}


# url for handle file upload
@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')

    save_path = "./"
    upload.save(save_path)
    return 'OK'


# url for handle nl generate
@route('/projects/<project>/vendors/<vendor>/nl', method='GET')
def nl(project, vendor):
    result = search_part_combine(project, vendor)
    return result


if __name__=="__main__":
    run(server='paste', host='10.99.40.253', port=80, debug=True, reloader=True)

