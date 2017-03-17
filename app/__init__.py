from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
db = SQLAlchemy(app)

from auth import model

bootstrap = Bootstrap(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'flaskimplement'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/travelplanner'

from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

app.debug = True



