import os
from glob import glob
from random import choice

from flask import Blueprint, abort, render_template, url_for

from app.event.models import Event
from config import basedir

album = Blueprint('album', __name__, url_prefix='/album')


@album.route('/show/<string:token>')
def index(token):
    """Для отображения страницы с альбомом!!!

    Parameters
    ----------
    token : string
        Токен доступа к альбому события

    Returns
    -------
    Flask.render_template
        Рендерит шаблон из папки шаблонов с заданным контекстом или 404
    """
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
