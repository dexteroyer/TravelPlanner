from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from forms import LoginForm, RegisterForm
from model import User, Role
from app import db, app
from decorators import required_roles

auth = Flask(__name__)
<<<<<<< HEAD
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates/users', static_folder='static',
                           static_url_path='static')
=======
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static',
                           static_url_path='/static/')

>>>>>>> de2c6e3ae0d186d2f15c0deb79d53bc31def63b9
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_blueprint.route('/home')
@login_required
@required_roles('User')
def home():
    return render_template('dashboard.html', username=current_user.username)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('You are now logged in!')
            return redirect(url_for('auth_blueprint.home', name=request.form['username']))
        else:
            error = 'Invalid username or password'
<<<<<<< HEAD
    return render_template('signin.html', form=form, error=error)
=======
    return render_template('users/signin.html', form=form, error=error)
  
>>>>>>> de2c6e3ae0d186d2f15c0deb79d53bc31def63b9

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    Role.insert_roles()
    if form.validate_on_submit():
        user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], role_id=1)
        db.session.add(user)
        db.session.commit()
        flash('Log In')
        return redirect(url_for('auth_blueprint.login'))
<<<<<<< HEAD
    return render_template('registration.html', form=form)
=======
    return render_template('users/registration.html', form=form)
>>>>>>> de2c6e3ae0d186d2f15c0deb79d53bc31def63b9

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('auth_blueprint.login'))