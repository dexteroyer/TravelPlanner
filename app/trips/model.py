from app import db

class Trips(db.Model):
    __tablename__ = "trips"
    tripID = db.Column(db.Integer, primary_key=True)
    tripName = db.Column(db.String(70))
    tripDateFrom = db.Column(db.Date)
    tripDateTo = db.Column(db.Date)

    def __init__(self, tripName, tripDateFrom, tripDateTo):
        self.tripName = tripName
        self.tripDateFrom = tripDateFrom
        self.tripDateTo = tripDateTo

    def __repr__(self):
        return '<tripName {}>'.format(self.tripName)



