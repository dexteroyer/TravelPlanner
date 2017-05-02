from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for
from flask_login import current_user
from forms import TripForm, ItineraryForm, EditTripForm
from model import Trips, Itineraries
from app import db

trip = Flask(__name__)
trip_blueprint = Blueprint('trip_blueprint', __name__, template_folder='templates', url_prefix='/trips',
                           static_folder='static',
                           static_url_path='/static/')


@trip_blueprint.route('/createtrip', methods=['GET', 'POST'])
def addtrip():
    error = None
    tripForm = TripForm()
    if request.method == 'POST':
        if tripForm.validate_on_submit():
            tripform = Trips(tripName=tripForm.trip_name.data,
                             tripDateFrom=tripForm.trip_date_from.data,
                             tripDateTo=tripForm.trip_date_to.data,
                             userID=current_user.id)

            db.session.add(tripform)
            db.session.commit()
            return redirect(url_for('trip_blueprint.addtrip'))

    return render_template('addtrip.html', form=tripForm, error=error)

@trip_blueprint.route('/', methods=['GET'])
def trips():
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
