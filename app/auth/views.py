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
from app.landing.views import landing_blueprint
from werkzeug import secure_filename
from PIL import Image
from app.trips.model import Trips

auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_blueprint.login'
login_manager.anonymous_user = Anonymous

img_folder = 'app/auth/static/images/'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------> START ADMIN
@auth_blueprint.route('/admin')
@login_required
@required_roles('Admin')
def addash():
    return render_template('admin/admindashboard.html')

@auth_blueprint.route('/admin/users/sort/<role_id>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortadmin(role_id):
    result = User.query.filter_by(role_id='1')
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/sort/moderator', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortmod():
    result = User.query.filter_by(role_id='2')
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/sort/user', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortuser():
    result = User.query.filter_by(role_id='3')
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def createuser():
    form = EditForm()
    return render_template('admin/createusers.html', form = form)

# USERS --> read
@auth_blueprint.route('/admin/users', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def manageusers():
    result = User.query.all()
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/create', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def createusers():
    form = EditForm()
    return render_template('admin/createusers.html', form=form)

#create
auth_blueprint.route('/admin/users/add', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def addusers():
    user = User(username=request.form['username'], role_id=request.form['role_id'], first_name=request.form['first_name'],
                last_name=request.form['last_name'], address=request.form['address'], city=request.form['city'],
                country=request.form['country'], birth_date=request.form['birth_date'], contact_num=request.form['contact_num'],
                description=request.form['description'])
    result = User.query.all()
    db.session.add(user)
    db.session.commit()
    flash("Your changes have been saved.")
    return render_template('admin/users.html', result=result)

#update
@auth_blueprint.route('/admin/users/edit/<username>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def editusers(username):
    user = User.query.filter_by(username=username).first()
    result = User.query.all()
    form = EditForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.address = form.address.data
        user.city = form.city.data
        user.country = form.country.data
        user.birth_date = form.birth_date.data
        user.contact_num = form.contact_num.data
        user.description = form.description.data
        db.session.add(user)
        db.session.commit()
        flash("Your changes have been saved.")
        return render_template('admin/users.html', result=result)
    else:
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.address.data = user.address
        form.city.data = user.city
        form.country.data = user.country
        form.birth_date.data = user.birth_date
        form.contact_num.data = user.contact_num
        form.description.data = user.description
        return render_template('admin/editusers.html', user=user, form=form)

#delete
@auth_blueprint.route('/admin/users/remove/<username>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def deleteusers(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    result = User.query.all()
    return render_template('admin/users.html', result = result)

# TRIPS --> read
@auth_blueprint.route('/admin/trips')
@login_required
@required_roles('Admin')
<<<<<<< HEAD
def adduser():
    #return redirect(url_for('auth_blueprint.createusers'))
    return render_template('admin/createusers.html')
=======
def managetrips():
    result = Trips.query.all()
    return render_template('admin/trips.html', result=result)
>>>>>>> 724d37450fc96ad32f6c1b00ded2cacf529b699a

#create
@auth_blueprint.route('/admin/trips/new')
@login_required
@required_roles('Admin')
def createtrip():
    form = TripForm()
    return render_template('admin/createtrip.html', form=form)

@auth_blueprint.route('/admin/trips/new/<tripName>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def addtrip(tripName):
    trips = Trips.query.filter_by(tripName=tripName).first()
    form = TripForm()
    trips.tripName = form.tripName.data
    trips.tripDateFrom = form.tripDateFrom.data
    trips.tripDateTo = form.tripDateTo.data
    trips.id = form.id.data
    trips.viewsNumber = form.viewsNumber.data
    trips.img_thumbnail = form.img_thumbnail.data
    db.session.add(trips)
    db.session.commit()
    flash("Your changes have been saved.")
    return render_template('admin/trips.html', result=result)

#update
@auth_blueprint.route('/admin/trips/edit/<tripName>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def edittrips(tripName):
    trips = Trips.query.filter_by(tripName=tripName).first()
    result = Trips.query.all()
    form = TripForm()
    if form.validate_on_submit():
        trips.tripName = form.tripName.data
        trips.tripDateFrom = form.tripDateFrom.data
        trips.tripDateTo = form.tripDateTo.data
        trips.id = form.id.data
        trips.viewsNumber = form.viewsNumber.data
        trips.img_thumbnail = form.img_thumbnail.data
        db.session.add(trips)
        db.session.commit()
        flash("Your changes have been saved.")
        return render_template('admin/trips.html', result=result)
    else:
        form.tripName.data = trips.tripName
        form.tripDateFrom.data = trips.tripDateFrom
        form.tripDateTo.data = trips.tripDateTo
        form.id.data = trips.id
        form.viewsNumber.data = trips.viewsNumber
        form.img_thumbnail.data = trips.img_thumbnail
        return render_template('admin/edittrips.html', trips=trips, form=form)

#delete
@auth_blueprint.route('/admin/trips/remove/<tripName>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def removetrips(tripName):
    trips = Trips.query.filter_by(tripName=tripName).first()
    db.session.delete(trips)
    db.session.commit()
    result = Trips.query.all()
    return render_template('admin/trips.html', result=result)

@auth_blueprint.route('/admin/connections')
@login_required
@required_roles('Admin')
def connections():
    return render_template('admin/connections.html')
# END ADMIN <----------

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
    Role.insert_roles(3)
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
