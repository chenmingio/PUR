import bottle
import jinja2

route = bottle.route
run = bottle.run
request = bottle.request
response = bottle.response
debug = bottle.debug
view = bottle.jinja2_view



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

if __name__=="__main__":
    run(server='paste', host='10.99.40.253', port=80, debug=True, reloader=True)

