import logging

from flask import Blueprint

blockchain = Blueprint('blockchain', __name__)

logger = logging.getLogger(__name__)

from app.blockchain import views
