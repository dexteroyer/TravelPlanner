from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import check_password_hash
from forms import LoginForm, RegisterForm, EditForm
from model import User, Role, Anonymous
from forms import LoginForm, RegisterForm, EditForm, SearchForm
from model import User, Role
<<<<<<< HEAD
from app import db, app, mail
from decorators import required_roles, get_friends, get_friend_requests, send_email
=======
from app import db, app

from decorators import required_roles, get_friends, get_friend_requests
<<<<<<< HEAD
=======
>>>>>>> c467f2f94e551be06f4b31e5175bf8599fa5ccd1
>>>>>>> 1cf7be276548e50cd65ed9b6451f3c6a28c6a688
>>>>>>> 053fa6dbe87ab296eb033033cd2debc4cd51bc32
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from sqlalchemy import func, desc

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

POSTS_PER_PAGE = 4

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def verify():
    label =[]
    if current_user.isAuthenticated():
        label = [current_user.username, "Log Out", "/home", "/logout"]
    else:
        label = ["Log In", "Sign Up", "/login", "/register"]
    return label

@auth_blueprint.route('/')
@auth_blueprint.route('/index')
def index():
    label=verify()
    users = User.query.order_by(desc(User.id)).paginate(1, POSTS_PER_PAGE, False)
    users_for_most = User.query.order_by(User.id).paginate(1, POSTS_PER_PAGE, False)
    return render_template('index.html', title='TravelPlanner-Home', users=users, user_m=users_for_most, label=label)
    #return '<h1><a href="/login">Sign In!</a> No account? <a href="/register">Sign Up!</a></h1>'

@auth_blueprint.route('/view/<username>', methods=['GET','POST'])
def mock(username):
    users = User.query.filter_by(username=username).first()
    label, links =[], []
    label = verify()
    return render_template('view_trip.html', title=users.username, users=users, label=label)

@auth_blueprint.route('/trip-plans/')
@auth_blueprint.route('/trip-plans/<linklabel>', methods=['GET','POST'])
def view_each(linklabel='all trips made in this site'):
    label=verify()
    til='Search Result'
    users = db.session.query(User).filter(func.concat(User.username, ' ', User.first_name, ' ', User.last_name, ' ', User.email, ' ', User.description).like('%'+linklabel+'%')).all()
    if linklabel=='most-popular':
        til='Most Popular'
        users = User.query.order_by(User.id).all()
        linklabel='Most Popular'
    elif linklabel=='newest-trip-plans':
        til='Newest Trips'
        users = User.query.order_by(desc(User.id)).all()
        linklabel='Newest Trip Plans'
    elif linklabel=='all trips made in this site':
        til='All Trips'
        users = User.query.order_by(User.id).all()
        linklabel='All Trips'
    elif linklabel=='filtered_result':
        user_ = []
        if request.args.get('option')=='all-trips':
            users = User.query.order_by(User.id).all()
        elif request.args.get('option')=='most-popular':
            users = User.query.order_by(User.id).all()
        elif request.args.get('option')=='newest-trip-plans':
            users = User.query.order_by(desc(User.id)).all()

        for user in users:
            if (request.args.get('country') in user.username) or (request.args.get('city') in user.email):
                user_.append(user)
        return render_template('trip-plans.html', title=til, users=user_, label=label, search_label=request.args.get('city'))
    return render_template('trip-plans.html', title=til, users=users, label=label, search_label=linklabel)

@app.route('/paginate/<int:index>')
def paginate(index):
    usernameL, emailL, descriptionL = [], [], []
    if index==1:
        page_string = request.args.get('page')
        users = User.query.order_by(desc(User.id)).paginate(int(page_string), POSTS_PER_PAGE, False)
    elif index==2:
        page_string = request.args.get('page_1')
        users = User.query.order_by(User.id).paginate(int(page_string), POSTS_PER_PAGE, False)

    for user in users.items:
        usernameL.append(user.username)
        emailL.append(user.email)
        descriptionL.append(user.description)
    determiner = users.has_next
    print determiner
    return jsonify(result1=usernameL, result2=emailL, result3=descriptionL, size=len(usernameL), determiner=determiner)

@auth_blueprint.route('/sendRepsonse')
def sendMail():
    body = "From: %s \n Email: %s \n Message: %s" % (request.args.get('name'), request.args.get('email'), request.args.get('body'))
    send_email('TravelPlanner', 'travelplannerSy@gmail.com', ['travelplannerSy@gmail.com'], body)
    return jsonify(sent=True)

@auth_blueprint.route('/admin')
@login_required
@required_roles('Admin')
def addash():
    return 'welcome!'

@auth_blueprint.route('/home')
@login_required
@required_roles('User')
def home():
    return render_template('users/dashboard.html', username=current_user.username)


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

@login_required
@required_roles('User')
def edit(username):
    user = User.query.filter_by(username=username).first()
    form = EditForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.birth_date = form.birth_date.data
        current_user.contact_num = form.contact_num.data
        current_user.description = form.description.data
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
        return redirect(url_for('auth_blueprint.index'))
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
                    return redirect(url_for('auth_blueprint.index'))
            else:
<<<<<<< HEAD
                error = 'Invalid username or password'
        return render_template('users/signin.html', form=form, error=error)
=======
                return redirect(url_for('auth_blueprint.index'))
        else:
            error = 'Invalid username or password'
<<<<<<< HEAD
=======
<<<<<<< HEAD

    return render_template('users/signin.html', form=form, error=error)
>>>>>>> 1cf7be276548e50cd65ed9b6451f3c6a28c6a688

>>>>>>> 053fa6dbe87ab296eb033033cd2debc4cd51bc32

    return render_template('users/signin.html', form=form, error=error)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    Role.insert_roles()
<<<<<<< HEAD
    if current_user.is_active():
        return redirect(url_for('auth_blueprint.index'))
    else:
        if form.validate_on_submit():
            user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], role_id=3)          
            db.session.add(user)
            db.session.commit()
            flash('Log In')
            return redirect(url_for('auth_blueprint.login'))
        return render_template('users/registration.html', form=form)
=======
    if form.validate_on_submit():
        user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], role_id=3)
        db.session.add(user)
        db.session.commit()
        flash('Log In')
        return redirect(url_for('auth_blueprint.login'))

    return render_template('users/registration.html', form=form)
>>>>>>> 1cf7be276548e50cd65ed9b6451f3c6a28c6a688

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
        return redirect(url_for('auth_blueprint.index'))

admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Trips, db.session))
admin.add_view(NotificationView(name='Notification', endpoint='notify'))
admin.add_view(Logout(name='Logout', endpoint='logout'))
