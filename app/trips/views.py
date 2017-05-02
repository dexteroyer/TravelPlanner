import os
from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, send_from_directory
from flask_login import current_user
from forms import TripForm, ItineraryForm, EditTripForm
from model import Trips, Itineraries
from app import db
<<<<<<< HEAD
=======
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from werkzeug import secure_filename
from PIL import Image
>>>>>>> 7647a4886305eff2d5fa68c7d7479140cc51a8b7

trip = Flask(__name__)
trip_blueprint = Blueprint('trip_blueprint', __name__, template_folder='templates', url_prefix='/trips',
                           static_folder='static',
                           static_url_path='/static/')

img_folder = 'app/trips/static/images/'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension

@trip_blueprint.route('/createtrip', methods=['GET', 'POST'])
def addtrip():
    error = None
    tripForm = TripForm()
    if request.method == 'POST':
        if tripForm.validate_on_submit():
            tripform = Trips(tripName=tripForm.trip_name.data,
                             tripDateFrom=tripForm.trip_date_from.data,
                             tripDateTo=tripForm.trip_date_to.data,
                             userID=current_user.id,
                             img_thumbnail=tripForm.file.data.filename)
            db.session.add(tripform)
            db.session.commit()

            if tripForm.file.data and allowed_file(tripForm.file.data.filename):
                filename = secure_filename(tripForm.file.data.filename)
                tripForm.file.data.save(os.path.join(img_folder+'trips/', filename))
            ex = os.path.splitext(filename)[1][1:]
            st = img_folder+'trips/'+filename
            img = Image.open(open(str(st), 'rb'))
            img.save(str(st), format=None, quality=50)

            return redirect(url_for('trip_blueprint.addtrip'))

    return render_template('addtrip.html', form=tripForm, error=error)

@trip_blueprint.route('/', methods=['GET'])
def trips():
<<<<<<< HEAD
    trip = Trips.query.filter_by(userID=current_user.id)
    return render_template('/trip.html', trips=trip)

@trip_blueprint.route('/<tripName>/edit', methods=['GET', 'POST'])
def editTrips(tripName):
    error = None
    tripname = Trips.query.filter_by(tripName=tripName).first()
    form = EditTripForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form = Itineraries(tripName=EditTripForm.trip_name.data,
                             tripDateFrom=EditTripForm.trip_date_from.data,
                             tripDateTo=EditTripForm.trip_date_to.data)
            db.session.add(form)
            db.session.commit()
            return redirect(url_for('trip_blueprint.editTrips'))
    return render_template('edittrip.html', tripname=tripname, error=error, form=form)


@trip_blueprint.route('/<tripName>/additineraries', methods=['GET', 'POST'])
def addItinerary(tripName):
    error = None
    itineraryForm = ItineraryForm()
    if request.method == 'POST':
        if itineraryForm.validate_on_submit():
            itineraryform = Itineraries(itineraryName=itineraryForm.itinerary_name.data,
                             itineraryDateFrom=itineraryForm.itinerary_date_from.data,
                             itineraryDateTo=itineraryForm.itinerary_date_to.data,
                             itineraryTimeFrom=itineraryForm.itinerary_time_from.data,
                             itineraryTimeTo=itineraryForm.itinerary_time_to.data,
                             tripID=tripName.tripID)
            db.session.add(itineraryform)
            db.session.commit()
            return redirect(url_for('trip_blueprint.addItinerary'))
    return render_template('addItinerary.html', form=itineraryForm, error=error)

@trip_blueprint.route('/<tripName>/itineraries', methods=['GET'])
def itineraries():
    error = None
    return render_template('addItinerary.html', error=error)
=======
    cursor = db.session.execute("""SELECT "tripName", "tripDateFrom", "tripDateTo" from "trips" WHERE "userID" = '{userID_}'""".format(userID_=current_user.id))
    return render_template('/trip.html', trips = cursor.fetchall())

>>>>>>> 7647a4886305eff2d5fa68c7d7479140cc51a8b7
