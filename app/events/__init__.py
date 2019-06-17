import logging

from flask import Blueprint

events = Blueprint('events', __name__)

logger = logging.getLogger(__name__)

from app.events import views, ajax
