from app import db

db.create_all()

# from app.auth.model import User

# name = User('name', 'name@name.com', 'name')
#
# db.session.add(name)
# db.session.commit()
#
# names = User.query.all()
# print names