from flask import Blueprint

events = Blueprint('events', __name__)

from app.events import views
