import os
import settings

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Основоной класс нвстроек
    """
    SECRET_KEY = os.urandom(24)

    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = os.urandom(24)

    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI =\
        f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    #  для email
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = settings.MAIL_USERNAME
    MAIL_PASSWORD = settings.MAIL_PASSWORD

    MAIL_DEFAULT_SENDER = settings.MAIL_USERNAME
    MAIL_CONFIRM_SALT = os.urandom(24)

    DEBUG = settings.DEBUG

    @staticmethod
    def init_app(app):
        pass
