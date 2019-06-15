from flask import render_template, abort

from app.events.models import Event

from . import album


@album.route('/show/<string:token>')
def index(token):

    if token:
        event_ = Event.query.filter_by(token=token).first()

        if event_ is None:
            return abort(404)

        return render_template('album.html', event=event_)
    else:
        return abort(404)
