from flask import Blueprint

auth_ = Blueprint('auth_', __name__)

from app.auth_ import views
