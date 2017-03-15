from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from auth.views import auth_blueprint

app.register_blueprint(auth_blueprint)

app.debug = True



