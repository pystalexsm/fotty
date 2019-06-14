import uuid
from datetime import datetime
from hashlib import sha256

from flask import jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import and_

from app.database import db
from app.events.models import Event, EventFiles

from . import events


@events.route('/ajax/bind/eventfile', methods=('POST',))
@login_required
def bind_event_and_photo():
    """
    Метод для добавления связей фото и события
    """

    if request.is_xhr:

        event_id = request.form.get('event_id')
        file_id = request.form.get('file_id')

        try:

            if event_id and file_id:

                event_id = int(event_id)
                file_id = int(file_id)

                check_file = EventFiles.query.filter(
                    and_(EventFiles.event_id.__eq__(event_id),
                         EventFiles.file_id.__eq__(file_id))).first()

                if check_file is None:
                    event_file = EventFiles(
                        file_id=file_id,
                        event_id=event_id,
                        created_at=datetime.now()
                    )

                    db.session.add(event_file)
                    db.session.commit()

                return jsonify(status=1, massage='OK')

        except (ValueError, TypeError):
            return jsonify(status=-1, massage='Не корректные данные')

        else:
            return jsonify(status=-1, massage='Не корректные данные')
    else:
        return jsonify(status=-1, massage='Данный метод можно вызвать только через ajax')


@events.route('/ajax/unbind/eventfile', methods=('POST',))
@login_required
def unbind_event_and_photo():
    """
    Метод для удаления связей фото и события
    """

    if request.is_xhr:

        event_id = request.form.get('event_id')
        file_id = request.form.get('file_id')

        try:

            if event_id and file_id:

                event_id = int(event_id)
                file_id = int(file_id)

                del_file = EventFiles.query.filter(
                    and_(EventFiles.event_id.__eq__(event_id),
                         EventFiles.file_id.__eq__(file_id))).first()

                if del_file is not None:
                    db.session.delete(del_file)
                    db.session.commit()

                return jsonify(status=1, massage='OK')

        except (ValueError, TypeError):
            return jsonify(status=-1, massage='Не корректные данные')

        else:
            return jsonify(status=-1, massage='Не корректные данные')
    else:
        return jsonify(status=-1, massage='Данный метод можно вызвать только через ajax')


@events.route('/ajax/generate/token', methods=('POST',))
@login_required
def generate_token_event():
    """
    Метод для генерации токена
    """

    event_id = request.form.get('event_id')
    user_id = current_user.get_id()

    if request.is_xhr:
        try:
            event_id = int(event_id)

            event_ = Event.query.filter(and_(
                Event.id.__eq__(event_id),
                Event.status.__eq__(Event.STATUS_ACTIVATE)
            )).first()

            if event_ is not None:
                string = f"{str(uuid.uuid4())}@--.{user_id}<>|]{event_id}"
                token = sha256(bytes(string, 'utf8')).hexdigest()
                if token:
                    event_.token = token
                    event_.update_at = datetime.now()

                    db.session.add(event_)
                    db.session.commit()

                    return jsonify(status=1, massage='OK')
            else:
                return jsonify(status=-1, massage='Событие не существует!')

        except (TypeError, ValueError):
            return jsonify(status=-1, massage='При генерации токена произошла ошиька!')
    else:
        return jsonify(status=-1, massage='Данный метод можно вызвать только через ajax')
