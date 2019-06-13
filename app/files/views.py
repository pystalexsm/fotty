from flask import jsonify, request
from PIL import Image

from . import files


@files.route('/upload', methods=('POST',))
def upload():
    WIDTH = 1200
    HEIGHT = 800

    file_ = request.files.get('file')
    if file_ is not None:
        try:
            with Image.open(file_) as im:
                print(file_, im.format, "%dx%d" % im.size, im.mode)
                im.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
                print(file_, im.format, "%dx%d" % im.size, im.mode)
                im.show()
        except IOError:
            pass

    return jsonify(status=1, data={'id': 1, 'filename': 'rrt'}), 200
