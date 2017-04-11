from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'flaskimplement'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/travelplanner'
app.config['WHOOSH_BASE'] = 'path/to/whoosh/base'