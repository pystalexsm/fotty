from flask import Blueprint

profile = Blueprint('profile', __name__)

from app.profile import views
