from pur_doc import app
import logging

logging.basicConfig(filename='./file.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    try:
        app.run(host='localhost', port=8080,
            debug=True, reloader=True)
    except Exception:
        logging.exception("Exception in main: ")

