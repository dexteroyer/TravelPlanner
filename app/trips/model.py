from app import db

class Trips(db.Model):
    __tablename__ = "trips"
    tripID = db.Column(db.Integer, primary_key=True)
    tripName = db.Column(db.String(70))
    tripDateFrom = db.Column(db.Date)
    tripDateTo = db.Column(db.Date)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    viewsNum = db.Column(db.Integer)
    img_thumbnail = db.Column(db.String(70))

    def __init__(self, tripName, tripDateFrom, tripDateTo, userID, img_thumbnail):
        self.tripName = tripName
        self.tripDateFrom = tripDateFrom
        self.tripDateTo = tripDateTo
        self.userID = userID
<<<<<<< HEAD
        self.viewsNum = 0
=======
        self.viewsNum = 0;
        self.img_thumbnail = img_thumbnail
>>>>>>> 7647a4886305eff2d5fa68c7d7479140cc51a8b7

    def __repr__(self):
        return '<tripName {}>'.format(self.tripName)

class Itineraries(db.Model):
    __tablename__ = "itineraries"
    itineraryID = db.Column(db.Integer, primary_key=True)
    itineraryName = db.Column(db.String(70))
    itineraryDesc = db.Column(db.String(1000))
    itineraryDateFrom = db.Column(db.Date)
    itineraryDateTo = db.Column(db.Date)
    tripID = db.Column(db.Integer, db.ForeignKey("trips.tripID"))




