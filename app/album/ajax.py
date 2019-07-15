from flask import Blueprint, request, jsonify
from datetime import datetime

from app.event.models import Client
from app.database import db


album_ajax = Blueprint('album_ajax', __name__, url_prefix='/album/ajax')


@album_ajax.route('/client', methods=('POST',))
def client():
    fingerprint = request.form.get('fingerprint')

    if fingerprint:
        fingerprint = fingerprint.strip()

        client_ = Client.query.filter_by(fingerprint=fingerprint).first()
        if not client_:
            client_ = Client(
                fingerprint=fingerprint,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            db.session.add(client_)
            db.session.commit()

    return jsonify(message='Ok'), 200
