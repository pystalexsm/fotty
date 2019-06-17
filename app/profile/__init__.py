import logging

from flask import Blueprint

profile = Blueprint('profile', __name__)

logger = logging.getLogger(__name__)

from app.profile import views
