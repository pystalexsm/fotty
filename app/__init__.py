from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager
from sqlalchemy import exc

from config import Config

login = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('/404.html', title=404), 404

    @login.user_loader
    def load_user(user_id):
        print(user_id)
        """
        проверка авторизации
        :param user_id: идентификатор пользователя
        :return: user | None
        """

        try:
            pass
        except exc.OperationalError:
            # логирование
            return None

        return None

    @login.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth_.login'))

    from app.auth_ import auth_ as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/')

    return app
