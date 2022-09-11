from flask import Blueprint

slash_cmds_bp = Blueprint('slash_cmds_bp', __name__)

from . import views
