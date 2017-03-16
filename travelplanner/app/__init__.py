from flask import Flask
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from auth.views import auth_blueprint

app.register_blueprint(auth_blueprint)
=======
import os

app = Flask(__name__)
app.debug = True

from app import views
>>>>>>> b4773bbf57b6564a26b75704e8b1ed77f81bcf2d
