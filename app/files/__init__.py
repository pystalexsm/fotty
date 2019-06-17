import logging

from flask import Blueprint

files = Blueprint('files', __name__)

logger = logging.getLogger(__name__)

from app.files import views
