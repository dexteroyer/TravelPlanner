from app import db
from app.auth.model import User


db.create_all()

db.session.commit()

