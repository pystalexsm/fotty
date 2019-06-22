import logging

from flask import Blueprint

event = Blueprint('event', __name__)

logger = logging.getLogger(__name__)

from app.event import views, ajax
