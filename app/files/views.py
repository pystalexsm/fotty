from flask import jsonify, request
from PIL import Image

from . import files


@files.route('/upload', methods=('POST',))
def upload():
    file_ = request.files.get('file')
    if file_ is not None:
        im = Image.open(file_)

    return jsonify(status=1, data={'id': 1, 'filename': 'rrt'}), 200
