from flask import Blueprint

auth_routes = Blueprint('auth', __name__)

from app.auth import routes