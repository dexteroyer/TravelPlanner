from flask import Flask, render_template, redirect, Blueprint, request, flash
from werkzeug.security import check_password_hash
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from .forms import LoginForm, RegisterForm
from .model import User


auth = Flask(__name__)
db = SQLAlchemy(auth)

auth_blueprint = Blueprint('auth', __name__)

@auth.blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('You are now logged in!')
        else:
            error = 'Invalid username or password'
    return render_template('login.html', form = form, error = error)