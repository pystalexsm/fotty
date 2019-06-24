from app.album.views import album as album_blueprint
from app.auth_.views import auth_ as auth_blueprint
from app.blockchain.views import blockchain as blockchain_blueprint
from app.event.views import event as event_blueprint
from app.event.ajax import event_ajax as event_ajax_blueprint
from app.files.views import files as files_blueprint
from app.profile.views import profile as profile_blueprint


def init_blueprint(app):
    """Для инициализации Blueprints

    Parameters
    ----------
    app :  application
        Приложение Flask

    Returns
    -------
    Flask
        Приложение Flask
    """

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(event_blueprint)
    app.register_blueprint(event_ajax_blueprint)
    app.register_blueprint(files_blueprint)
    app.register_blueprint(album_blueprint)
    app.register_blueprint(blockchain_blueprint)

    return app
