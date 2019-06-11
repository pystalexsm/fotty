from datetime import datetime

from app.database import db


class User(db.Model):

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

    def is_active(self):
        """True, as all users are active."""
        return self.confirmed

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<User %r>' % self.name
