from datetime import datetime

from app.database import db


class Event(db.Model):

    """
    Модель событий
    """

    __tablename__ = 'events'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='ID события')
    name = db.Column(db.String(255), nullable=False, comment='Название события')
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False, comment='ID пользователя')
    date_at = db.Column(db.String(255), nullable=False, default=datetime.now(), comment='Дата события')
    place = db.Column(db.String(255), nullable=False, comment='Место')
    status = db.Column(db.Integer, nullable=False, comment='Статус', default=1)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создвния')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата обновления')

    def __repr__(self):
        return '<Event %r>' % self.name
