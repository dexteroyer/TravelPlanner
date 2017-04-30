import os
from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import check_password_hash
from forms import LoginForm, RegisterForm, EditForm
from model import User, Role, Anonymous
from forms import LoginForm, RegisterForm, EditForm, SearchForm
from model import User, Role
from app import db, app
from decorators import required_roles, get_friends, get_friend_requests, allowed_file
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from app.landing.views import landing_blueprint
from werkzeug import secure_filename
from PIL import Image

auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import BaseView, expose

# admin = Admin(app, template_mode='bootstrap3')

admin = Admin(app, template_mode='bootstrap3')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_blueprint.login'
login_manager.anonymous_user = Anonymous

img_folder = 'app/auth/static/images/'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_blueprint.route('/admin')
@login_required
@required_roles('Admin')
def addash():
    return 'welcome!'

@auth_blueprint.route('/home')
@login_required
@required_roles('User')
def home():
    return render_template('users/dashboard.html', username=current_user.username, profile=current_user.profile_pic)


@auth_blueprint.route('/new-trip')
@login_required
@required_roles('User')
def new_trip():
    return render_template('users/trip.html')

@auth_blueprint.route('/friends', methods=['GET','POST'])
@login_required
@required_roles('User')
def show_friends():
    """Show friend requests and list of all friends"""
    form = SearchForm()
    # This returns User objects for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests("current_user.id")

    # This returns a query for current user's friends (not User objects), but adding .all() to the end gets list of User objects
    friends = get_friends("current_user.id").all()

    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('auth_blueprint.show_friends'))
    return render_template("users/friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends,
                           query=form.search.data,
                           form=form)


@auth_blueprint.route("/friends/search/<query>", methods=["GET", "POST"])
@login_required
@required_roles('User')
def search_users(query):
    """Search for a user and return results."""
    form = SearchForm()
    # Returns users for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests("current_user.id")

    # Returns query for current user's friends (not User objects) so add .all() to the end to get list of User objects
    friends = get_friends("current_user.id").all()

    #user_input = request.args.get("q")
    # Search user's query in users table of db and return all search results
    #search_results = search(db.session.query(User), user_input).all()
    results = User.query.whoosh_search(query).all()

    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('auth_blueprint.search_users'))
    return render_template("users/browse_friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends,
                           query=query,
                           form=form,
                           results=results)

@auth_blueprint.route('/userprofile/<username>')
@login_required
@required_roles('User')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('users/userprofile.html', user=user)

@auth_blueprint.route('/userprofile/<username>/edit', methods=['GET', 'POST'])
@auth_blueprint.route('/userprofile/edit/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('User')
def edit(username):
    user = User.query.filter_by(username=username).first()
    form = EditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.address = form.address.data
            current_user.city = form.city.data
            current_user.country = form.country.data
            current_user.birth_date = form.birth_date.data
            current_user.contact_num = form.contact_num.data
            current_user.description = form.description.data

            if form.file.data.filename==None or form.file.data.filename=='':
                current_user.profile_pic = current_user.profile_pic
            else:
                if(current_user.profile_pic=='default'):
                    pass
                else:
                    os.remove(img_folder+'users/'+str(current_user.profile_pic))

                current_user.profile_pic=form.file.data.filename

                if form.file.data and allowed_file(form.file.data.filename):
                    filename = secure_filename(form.file.data.filename)
                    form.file.data.save(os.path.join(img_folder+'users/', filename))
                ex = os.path.splitext(filename)[1][1:]
                st = img_folder+'users/'+filename
                img = Image.open(open(str(st), 'rb'))
                img.save(str(st), format=None, quality=50)

            db.session.add(current_user)
            db.session.commit()


            flash("Your changes have been saved.")
            return render_template('users/userprofile.html', user=user)
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.birth_date.data = current_user.birth_date
        form.contact_num.data = current_user.contact_num
        form.description.data = current_user.description
        return render_template('users/edit_profile.html', user=user, form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if current_user.is_active():
        return redirect(url_for('landing_blueprint.index'))
    else:
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(username=request.form['username']).first()
                if user.role_id == 3:
                    if user is not None and check_password_hash(user.password, request.form['password']):
                        login_user(user)
                        flash('You are now logged in!')
                    if user.first_login == True:
                        user.first_login = False
                        db.session.add(user)
                        db.session.commit()
                        return redirect(url_for('auth_blueprint.edit', username=request.form['username']))
                    return redirect(url_for('auth_blueprint.home', name=request.form['username']))
                elif user.role_id == 1:
                    if user is not None and check_password_hash(user.password, request.form['password']):
                        login_user(user)
                        flash('You are now logged in!')
                    return redirect(url_for('auth_blueprint.addash', name=request.form['username']))
                else:
                    return redirect(url_for('landing_blueprint.index'))
            else:
                error = 'Invalid username or password'
                return render_template('users/signin.html', form=form, error=error)
        else:
            error = 'Invalid username or password'
        return render_template('users/signin.html', form=form, error=error)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    Role.insert_roles()
    if current_user.is_active():
        return redirect(url_for('landing_blueprint.index'))
    else:
        if form.validate_on_submit():
            user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], role_id=3)          
            db.session.add(user)
            db.session.commit()
            flash('Log In')
            return redirect(url_for('auth_blueprint.login'))
        return render_template('users/registration.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('auth_blueprint.login'))

class NotificationView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notify.html')

class Logout(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('landing_blueprint.index'))

admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Trips, db.session))
admin.add_view(NotificationView(name='Notification', endpoint='notify'))
admin.add_view(Logout(name='Logout', endpoint='logout'))
