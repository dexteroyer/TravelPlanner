from flask import Flask
import os


_basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.secret_key = "flask"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:8080/db'