from flask import Blueprint

files = Blueprint('files', __name__)

from app.files import views
