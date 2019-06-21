from . import blockchain, logger
from flask import Markup


@blockchain.route('/')
def index():
    return Markup(f"<p>Вы попали в новый модуль {__name__}!</p><p><a href='/'>Скорей на главную!</a></p>")
