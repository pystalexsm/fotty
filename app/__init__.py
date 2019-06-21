import locale
import logging
import os
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from flask import Flask, current_app, redirect, render_template, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import exc, and_

from app.auth_.models import User
from app.database import db
from app.email import mail
from app.events.models import Event, EventFiles
from app.files.models import Files
from config import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_BACKEND_URL)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

login = LoginManager()
migrate = Migrate()

logging.basicConfig(filename='error.log', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

# TODO узнать, можно ли вынести методы связанные с celery?
@celery.task(name='files.clear_files_not_entitys')
def clear_files_not_entitys():
    """Задача. Чекает файлы, если файл за 2 суток не привязан к сущности, то он удалиться

    Returns
    -------
    Boolean
        Возвращает boolean
    """

    rows = db.session.query(
        Files, EventFiles).outerjoin(
        EventFiles, EventFiles.file_id.__eq__(Files.id)).filter(
        and_(
            (Files.created_at.__lt__(
                datetime.now() - timedelta(days=current_app.config['FILE_LIFE_TIME_NOT_CONFIRMED']))),
            EventFiles.file_id.__eq__(None))).all()

    try:
        if rows:
            for file, entity in rows:
                full_path_del_file = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
                if os.path.exists(full_path_del_file):
                    os.remove(full_path_del_file)
                db.session.delete(file)
            db.session.commit()
    except Exception as ex:  # TODO уточнить исключения.
        logger.exception(ex)
        return False

    return True


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Ставим задачи по расписанию для celerybeat
    """
    sender.add_periodic_task(crontab(minute=0, hour=1), clear_files_not_entitys.s())


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)

    celery.conf.update(app.config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login.init_app(app)

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Event=Event, Files=Files, EventFiles=EventFiles)

    @app.context_processor
    def init():
        return {
            'now': datetime.now()
        }

    @app.template_filter('formatdatetime')
    def format_datetime(value, format="%d %B, %Y %H:%M"):
        """Format a date time to (Default): %d %B, %Y %H:%M"""
        if value is None:
            return ""
        return value.strftime(format)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('/404.html', title=404), 404

    @login.user_loader
    def load_user(user_id):
        """
        проверка авторизации
        :param user_id: идентификатор пользователя
        :return: user | None
        """

        try:
            user_ = User.query.filter_by(id=int(user_id)).first()
            if user_ is not None:
                return user_
        except (exc.OperationalError, TypeError) as ex:
            # логирование
            logging.exception(ex)
            return None

        return None

    @login.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth_.login'))

    from app.auth_ import auth_ as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/')

    from app.events import events as events_blueprint
    app.register_blueprint(events_blueprint, url_prefix='/events')

    from app.files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix='/files')

    from app.album import album as album_blueprint
    app.register_blueprint(album_blueprint, url_prefix='/album')

    from app.blockchain import blockchain as blockchain_blueprint
    app.register_blueprint(blockchain_blueprint, url_prefix='/blockchain')

    return app
