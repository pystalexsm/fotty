from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import and_

from app.event.models import Client, EventViews
from app.database import db


album_ajax = Blueprint('album_ajax', __name__, url_prefix='/album/ajax')


@album_ajax.route('/client', methods=('POST',))
def client():
    """Для идентификации клиента и фиксации просмртра

    :param fingerprint: Идентификатор клиента
    :type fingerprint: string

    :param event_id: Идентификатор события
    :type event_id: integer

    :return: message, status
    :rtype: jsonify
    """
    fingerprint = request.form.get('fingerprint')
    event_id = request.form.get('event_id')

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

        if client_ and event_id:
            views_ = EventViews.query.filter(
                and_(EventViews.client_id.__eq__(client_.id),
                     EventViews.event_id.__eq__(event_id))).first()
            if not views_:
                views_ = EventViews(
                    client_id=client_.id,
                    event_id=event_id,
                    created_at=datetime.now(),
                    cnt=0,
                )

            views_.cnt += 1
            views_.updated_at = datetime.now()

            db.session.add(views_)
            db.session.commit()

    return jsonify(message='Ok'), 200
