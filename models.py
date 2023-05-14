from flask_security import RoleMixin, UserMixin
from datetime import datetime
from app import db

# create table in database for assigning roles
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.roleId')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    gender = db.Column(db.Boolean()) #1 is Male, 0 is Female
    active = db.Column(db.Boolean(), nullable=False, default=1)
    birthdate = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    height = db.relationship('UserHeight', backref='user', lazy=True)
    weight = db.relationship('UserWeight', backref='user', lazy=True)
    tdee = db.relationship('UserTDEE', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref='role')

# create table in database for storing roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    roleId = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class UserHeight(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recId = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class UserWeight(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recId = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class UserTDEE(db.Model):
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recId = db.Column(db.Integer, primary_key=True)
    tdee = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Food(db.Model):
    foodId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    calo = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)