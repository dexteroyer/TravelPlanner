from app import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import backref

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    roles = db.relationship('Role', back_populates='users')

    
    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role_id = role_id

    def getRole_id(self):
        return self.role_id

    def getRole_name(self):
        role_name = Role.query.filter_by(id=self.getRole_id()).first()
        return role_name.name
        
    def __repr__(self):
        return '<username {}>'.format(self.username)

# class Role(db.Model):
#     __tablename__ = "role"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(15), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', back_populates='roles')
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<name {}>' .format(self.name)

    @staticmethod
    def insert_roles():
        roles = ['Admin', 'Moderator', 'User']
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()





