import os

from flask import Flask, send_from_directory, request
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')


ALLOWED_EXTENSIONS = ['jpg']
UPLOAD_FOLDER = '/uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "ok"
    else:
        return "error: no file or file not allowed"


@app.route('/upload_bitmap', methods=['POST'])
def upload_bitmap():
    return "todo"  # TODO


@app.route('/')
def send_index():
    return send_from_directory('static', "index.html")


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
