import os
import uuid
from datetime import datetime
from hashlib import md5

from flask import current_app, jsonify, request, url_for
from flask_login import login_required
from PIL import Image

from app.database import db
from app.files.models import Files

from . import files, logger


@files.route('/upload', methods=('POST',))
@login_required
def upload():
    WIDTH = 1200
    HEIGHT = 800

    source = request.files.get('file')
    if source is not None:
        try:
            with Image.open(source) as im:

                checksum = md5(im.tobytes()).hexdigest()
                filename = f"{str(uuid.uuid4())}.{im.format.lower()}"
                content_type = im.get_format_mimetype()

                if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'])):
                    os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER']))

                file_ = Files.query.filter_by(checksum=checksum).first()
                if file_ is None:

                    file_ = Files(
                        filename=filename,
                        content_type=content_type,
                        checksum=checksum,
                        created_at=datetime.now()
                    )

                    im.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
                    im.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    # TODO пока что так, нужно узнать другой варик!!!
                    size = os.stat(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)).st_size

                    file_.size = size

                    db.session.add(file_)
                    db.session.commit()

                else:
                    if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], file_.filename)) is False:
                        im.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
                        im.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_.filename))

        except (IOError, ValueError, FileNotFoundError, TypeError) as ex:
            logger.exception(ex)
            return jsonify(status=-1, message='При загрузки файлов произошла ошибка!'), 200

    return jsonify(
        status=1, message='OK',
        data={'id': file_.id, 'filename': file_.filename,
              'url': url_for('static', filename=f'files/{file_.filename}')}), 200
