from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, session
from werkzeug.security import check_password_hash
from forms import LoginForm
from model import User

auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static',
                           static_url_path='/static/')

@auth_blueprint.route('/')
def flask():
    return "Hello World!"

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                flash('You are now logged in!')
                return redirect(url_for(''))
        else:
            error = 'Invalid username or password'
    return render_template('signin.html', form=form, error=error)

@auth_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for(''))