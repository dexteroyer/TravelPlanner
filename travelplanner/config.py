from flask import Flask

import os


_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'pymysql+mysql://root@127.0.0.1:5000/travelplanner'
