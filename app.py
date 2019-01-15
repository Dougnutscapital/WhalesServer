import json
import os

from flask import Flask, send_from_directory, request
from flask import jsonify
from werkzeug.utils import secure_filename
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, static_url_path='')

app.config['ALLOWED_EXTENSIONS'] = ['jpg']
app.config['UPLOAD_FOLDER'] = './uploads'


label_dict = {}

with open("labels.json", 'r') as label_file:
    info = label_file.readline()
    label_dict = json.loads(info)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    app.logger.info('Filename: %s', file.filename)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        key = "865c2ba"  # only for demonstration
        if key in label_dict:
            files = label_dict[key]
            urls = ["train/" + f for f in files]
            return jsonify(urls)
        else:
            return "no matched images"
    else:
        return "error: no file or file not allowed"


@app.route('/upload_bitmap', methods=['POST'])
def upload_bitmap():
    return "todo"  # TODO

@app.route('/')
def send_index():
    return send_from_directory('static', "index.html")

@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('uploads', path)

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
