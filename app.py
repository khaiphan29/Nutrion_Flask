from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import required libraries from flask_login and flask_security
from flask_login import LoginManager
from flask_security import Security, SQLAlchemySessionUserDatastore

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy() 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-123123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite'

db.init_app(app)
from models import *

migrate = Migrate(app, db)

# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

# #login configuration
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our user table, use it in the query for the user
#     return User.query.get(user_id)

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for admin of app
from admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)