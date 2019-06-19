import bottle
import jinja2
import db

route = bottle.route
run = bottle.run
request = bottle.request
response = bottle.response
debug = bottle.debug
view = bottle.jinja2_view

nl_search_part = db.nl_search_part
nl_search_part_year = db.nl_search_part_year
nl_search_invest = db.nl_search_invest


@route('/')
@view('upload.html', template_lookup=['templates'])
def index():
    return {'title': "hello"}

@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('upload')

    save_path = "./"
    upload.save(save_path)
    return 'OK'

@route('/projects/<project>/vendors/<vendor>/nl', method='GET')
def nl(project, vendor):
    r = nl_search_part(project, vendor)
    print(r.keys())
    return {'vendor': vendor}


if __name__=="__main__":
    run(server='paste', host='10.99.40.253', port=80, debug=True, reloader=True)

