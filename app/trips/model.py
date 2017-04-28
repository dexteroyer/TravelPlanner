from app import db

class Trips(db.Model):
    __tablename__ = "trips"
    tripID = db.Column(db.Integer, primary_key=True)
    tripName = db.Column(db.String(70))
    tripDateFrom = db.Column(db.Date)
    tripDateTo = db.Column(db.Date)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    viewsNum = db.Column(db.Integer)

    def __init__(self, tripName, tripDateFrom, tripDateTo, userID):
        self.tripName = tripName
        self.tripDateFrom = tripDateFrom
        self.tripDateTo = tripDateTo
        self.userID = userID
        self.viewsNum = 0;

    def __repr__(self):
        return '<tripName {}>'.format(self.tripName)



