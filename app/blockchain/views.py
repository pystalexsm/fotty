import logging

from flask import Blueprint, Markup

blockchain = Blueprint('blockchain', __name__, url_prefix='/blockchain')

logger = logging.getLogger(__name__)


@blockchain.route('/')
def index():
    return Markup(f"<p>Вы попали в новый модуль {__name__}!</p><p><a href='/'>Скорей на главную!</a></p>")
