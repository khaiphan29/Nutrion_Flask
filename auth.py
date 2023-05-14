from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import *

auth = Blueprint('auth', __name__)

@auth.route("/userlogin", methods=["POST"])
def login():
    # search user in database
    user = User.query.filter_by(email=request.form['email']).first()

    # if exist check password
    if not user or not check_password_hash(user.password, request.form.get("password")) or user.roles[0].name != "User":
        msg="Login information is not matched."
        return render_template('index.html', msg=msg)
 
    #if login fails due to user is inactive
    if not login_user(user):
        msg="User is inactive."
        return render_template('index.html', msg=msg)
    
    return redirect(url_for('main.profile'))

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/register", methods=["POST"])
def register_post():
    # search user in database
    user = User.query.filter_by(email=request.form['email']).first()

    if user:
        flash('Email existed.')
        return redirect(url_for("main.index"))
    
    #find the role
    role = Role.query.filter_by(name="User").first()

    # store the user to database
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    gender = bool(request.form.get("gender"))
    birthdate = request.form.get("birthdate").split("-")
    user = User(email=email, password=generate_password_hash(password, method='scrypt'), name=name, active=1, gender=gender,  birthdate=datetime(int(birthdate[0]),int(birthdate[1]),int(birthdate[2])))
    
    user.roles.append(role)
        
    # commit the changes to database
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for("main.profile"))

@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("main.index"))