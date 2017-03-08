from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(os.environ['APP_SETTINGS'])


from auth.views import auth_blueprint

app.register_blueprint(auth_blueprint)