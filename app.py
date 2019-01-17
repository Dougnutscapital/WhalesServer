import json
import os
import time
import base64
import random

from flask import Flask, send_from_directory, request
from flask import jsonify
from werkzeug.utils import secure_filename
from logging.config import dictConfig

from classify import predict
from sketch_classify import predict_from_sketch

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
app.config['UPLOAD_FOLDER'] = os.path.join('', 'uploads')
app.config['SKETCH_FOLDER'] = os.path.join('', 'sketches')

label_dict = {}

with open("metadata/labels.json", 'r') as label_file:
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
        filename = str(round(time.time())) + secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path
    else:
        return "error: no file or file not allowed"


@app.route('/draw', methods=['POST'])
def query_sketch():
    file = request.form['image']
    file = file[str(file).index(',')+1:]
    if file:
        filename = str(round(time.time())) + ".jpg"
        file_path = os.path.join(app.config['SKETCH_FOLDER'], filename)
        with open(file_path, "wb") as fh:
            fh.write(base64.decodebytes(str.encode(file)))

        key = predict_from_sketch(file_path)[0]
        if key.startswith("w_"):
            key = key[2:]
        if key in label_dict:
            files = label_dict[key]
            urls = ["train/" + f for f in files]
            random.shuffle(urls)
            return jsonify(urls)
        else:
            return "error: no match"
    else:
        return "error: no file uploaded"


@app.route('/query/<path:path>', methods=['GET'])
def query_image(path):
    # TODO: query image
    path = os.path.join(app.config['UPLOAD_FOLDER'], path)
    if os.path.isfile(path):
        # TODO: query
        # key = "865c2ba"  # only for demonstration
        key = predict(path)[0]
        if key.startswith("w_"):
            key = key[2:]
        if key in label_dict:
            files = label_dict[key]
            urls = ["train/" + f for f in files]
            random.shuffle(urls)
            return jsonify(urls)
        else:
            return "no matched images"
        # TODO: delete, for frontend test
        # print(path)
        # urls = [path,path,path,path]
        # return jsonify(urls)
    else:
        return "file invalid"


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
