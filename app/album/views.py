import os
from glob import glob
from random import choice

from flask import abort, render_template, url_for

from app.events.models import Event
from config import basedir

from . import album


@album.route('/show/<string:token>')
def index(token):

    if token:
        event_ = Event.query.filter_by(token=token).first()

        if event_ is None:
            return abort(404)

        background_list = glob(os.path.join(basedir, 'app', 'static', 'images', 'background', '*.jp*g'))
        string_url_img = choice(background_list)

        list_url = string_url_img.split('/')
        if len(list_url) > 0:
            img_background = list_url[-1]

        if img_background:
            event_.background = url_for('static', filename=f'images/background/{img_background}')

        return render_template('album.html', event=event_)
    else:
        return abort(404)
