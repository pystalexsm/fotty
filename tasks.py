#!/usr/bin/env python3
import logging
import os
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import and_

from app import create_app
from app.database import db
from app.event.models import EventFiles
from app.files.models import Files

logger = logging.getLogger(__name__)

flask_app = create_app()

celery_app = Celery(
    __name__, broker=flask_app.config['CELERY_BROKER_URL'],
    backend=flask_app.config['CELERY_BACKEND_URL'])


@celery_app.task
def clear_files_not_entitys():
    """Задача. Чекает файлы, если файл за 2 суток не привязан к сущности, то он удалиться

    Returns
    -------
    Boolean
        Возвращает boolean
    """
    with flask_app.app_context():
        rows = db.session.query(
            Files, EventFiles).outerjoin(
            EventFiles, EventFiles.file_id.__eq__(Files.id)).filter(
            and_(
                (Files.created_at.__lt__(
                    datetime.now() - timedelta(days=flask_app.config['FILE_LIFE_TIME_NOT_CONFIRMED']))),
                EventFiles.file_id.__eq__(None))).all()

        try:
            if rows:
                for file, entity in rows:
                    full_path_del_file = os.path.join(flask_app.config['UPLOAD_FOLDER'], file.filename)
                    if os.path.exists(full_path_del_file):
                        os.remove(full_path_del_file)
                    db.session.delete(file)
                db.session.commit()
        except Exception as ex:  # TODO уточнить исключения.
            logger.exception(ex)
            return False

        return True


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Ставим задачи по расписанию для celerybeat
    """
    sender.add_periodic_task(crontab(minute=0, hour=1), clear_files_not_entitys.s())
