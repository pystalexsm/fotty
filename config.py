import os
import settings

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Основоной класс нвстроек
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))

    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  для email
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = settings.MAIL_USERNAME
    MAIL_PASSWORD = settings.MAIL_PASSWORD

    MAIL_DEFAULT_SENDER = 'radio@adeptum.ru'
    MAIL_CONFIRM_SALT = os.urandom(24)

    DEBUG = settings.DEBUG

    @staticmethod
    def init_app(app):
        pass
