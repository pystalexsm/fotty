from datetime import datetime

from flask_login import UserMixin

from app.database import db


class User(db.Model, UserMixin):

    """
    Модель пользователей
    """

    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='ID пользователя')
    name = db.Column(db.String(255), nullable=False, comment='Имя пользователя')
    phone = db.Column(db.String(255), nullable=False, comment='Телефон пользователя')
    email = db.Column(db.String(255), nullable=False, unique=True, comment='Email пользователя')
    password = db.Column(db.String(255), nullable=False, comment='Пароль пользователя')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создания')
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата обновления')
    confirmed = db.Column(db.Boolean(), default=False, comment='Подтвержден?')

    def __repr__(self):
        return '<User %r>' % self.name
