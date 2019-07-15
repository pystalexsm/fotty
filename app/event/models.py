from datetime import datetime

from app.database import db


class Event(db.Model):

    """
    Модель событий
    """

    STATUS_ACTIVATE = 1
    STATUS_DELETE = 2

    __tablename__ = 'events'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='ID события')
    title = db.Column(db.String(255), nullable=False, comment='Название события')
    user_id = db.Column(
        db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False, comment='ID пользователя')
    date_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата события')
    place = db.Column(db.String(255), nullable=False, comment='Место')
    token = db.Column(db.String(500), nullable=True, index=True, unique=True,
                      default='', comment='Токен доступа в альбому с фото')
    status = db.Column(db.Integer, nullable=False, comment='Статус', default=1)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создвния')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата обновления')
    files = db.relationship('EventFiles', order_by="asc(EventFiles.sort)")  # todo уточнить, как лучше делать!!!

    def __repr__(self):
        return '<Event %r>' % self.title


class EventFiles(db.Model):
    """
    Модель связей файла с сущностью
    """

    __tablename__ = 'event_files'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False,
                   autoincrement=True, comment='Id связи сущности и файла')
    file_id = db.Column(
        db.BigInteger, db.ForeignKey('files.id', ondelete='CASCADE'), index=True, nullable=False, comment='Id файла')
    event_id = db.Column(
        db.BigInteger, db.ForeignKey('events.id', ondelete='CASCADE'), index=True, nullable=False, comment='Id сущности')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создания')
    sort = db.Column(db.Integer, nullable=True, comment='Для сортировка фотографий')
    file_data = db.relationship('Files')

    def __repr__(self):
        return '<EventFiles %r>' % self.id
