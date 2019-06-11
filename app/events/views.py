from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.events.models import Event

from . import events
from app.database import db


@events.route('/')
@login_required
def index():
    return render_template('events.html', user=current_user)


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
            date_at = datetime.strptime(date_at, '%d-%m-%Y')

        if place is not None and len(place) > 0:
            place = place.strip()

        print(date_at)
        print(title)
        print(place)

        if title and date_at and place:
            event_ = Event()

            event_.name = title
            event_.date_at = date_at
            event_.place = place
            event_.status = 1
            event_.created_at = datetime.now()
            event_.updated_at = datetime.now()
            event_.user_id = current_user.get_id()

            db.session.add(event_)
            db.sesion.commit()

            return redirect(url_for('.events'))
        else:
            flash('Данные не прошли проверку!!!')

    return render_template('event-create-edit.html')
