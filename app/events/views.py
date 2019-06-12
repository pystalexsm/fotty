from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_

from app.database import db
from app.events.models import Event

from . import events


@events.route('/')
@login_required
def index():

    events_ = Event.query.filter_by(status=Event.STATUS_ACTIVATE).all()

    return render_template('events.html', user=current_user, events=events_, title='Список событий')


@events.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    if request.method.__eq__('POST'):

        title = request.form.get('title')
        date_at = request.form.get('date_at')
        place = request.form.get('place')

        if title is not None and len(title) > 0:
            title = title.strip()

        if date_at is not None and len(date_at) > 0:
            date_at = datetime.strptime(date_at, '%d.%m.%Y')

        if place is not None and len(place) > 0:
            place = place.strip()

        if title and date_at and place:

            event_ = Event(
                title=title,
                date_at=date_at,
                place=place,
                status=1,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=current_user.get_id()
            )

            db.session.add(event_)
            db.session.commit()

            return redirect(url_for('.index'))
        else:
            flash('Данные не прошли проверку!!!')

    return render_template('event-create.html', title="Создание события")


@events.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    user_id = current_user.get_id()
    event_ = Event.query.filter(and_(Event.id.__eq__(id), Event.user_id.__eq__(user_id))).first()

    if request.method.__eq__('POST'):

        title = request.form.get('title')
        date_at = request.form.get('date_at')
        place = request.form.get('place')

        if title is not None and len(title) > 0:
            title = title.strip()

        if date_at is not None and len(date_at) > 0:
            date_at = datetime.strptime(date_at, '%d.%m.%Y')

        if place is not None and len(place) > 0:
            place = place.strip()

        if title and date_at and place:

            event_.title = title
            event_.date_at = date_at
            event_.place = place
            event_.updated_at = datetime.now()

            db.session.add(event_)
            db.session.commit()

            return redirect(url_for('.index'))

        else:
            flash('Данные не прошли проверку!!!')

    return render_template('event-edit.html', event=event_, title=f'Редауьтрование события № {id}')


@events.route('/delete/<int:id>')
@login_required
def delete(id):
    if id:
        try:

            id = int(id)
            user_id = current_user.get_id()

            event_ = Event.query.filter(and_(Event.id.__eq__(id), Event.user_id.__eq__(user_id))).first()
            if event_ is not None:
                event_.status = Event.STATUS_DELETE
                event_.updated_at = datetime.now()

                db.session.add(event_)
                db.session.commit()

                flash(f'Успешное удаление события № {id}')

                return redirect(url_for('events.index'))

        except (TypeError, ValueError):
            flash('При удалении произошла ошибка!!!')
            return redirect(url_for('events.index'))

    flash('При удалении произошла ошибка!!!')
    return redirect(url_for('events.index'))
