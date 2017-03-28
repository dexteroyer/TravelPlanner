from flask import Blueprint
from app import db

auth = Blueprint('auth', __name__, template_folder='templates/users', static_folder='static')






