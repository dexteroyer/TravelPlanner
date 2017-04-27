from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for
from flask_login import current_user
from forms import TripForm
from model import Trips
from app import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

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
    cursor = db.session.execute("""SELECT "tripName", "tripDateFrom", "tripDateTo" from "trips" WHERE "userID" = '{userID_}'""".format(userID_=current_user.id))
    return render_template('/trip.html', trips = cursor.fetchall())
