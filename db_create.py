from app import app, db
db.create_all()
# with app.app_context():
#     db.create_all()
    
#db.create_all()

# from app.auth.model import User
#
# name = User('name', 'name@name.com', 'name')
# name2 = User('name2', 'name2@name2.com', 'name2')
#
# db.session.add(name)
# db.session.add(name2)
# db.session.commit()
#
# names = User.query.all()
# print names