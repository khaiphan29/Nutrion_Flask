from flask import Blueprint, render_template, redirect, request, url_for, flash
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from flask_security import roles_accepted
from models import *

admin = Blueprint('admin', __name__)

@admin.route("/admin")
def admin_login():
    if not current_user.is_authenticated:
        return render_template("admin.html")
    
    if current_user.roles[0].name == "Admin":
        return redirect(url_for("admin.admin_profile"))
    return redirect(url_for("main.profile"))
    

@admin.route("/admin", methods=["POST"])
def admin_login_post():
    # search user in database
    user = User.query.filter_by(email=request.form['email']).first()

    # if exist check password
    if not user or not check_password_hash(user.password, request.form.get("password")):
        msg="Login information is not matched."
        return render_template('admin.html', msg=msg)
    #check roles
    if user.roles[0].name != "Admin":
        return redirect(url_for("main.index"))
 
    #if login fails due to user is inactive
    if not login_user(user):
        msg="User is inactive."
        return render_template('admin.html', msg=msg)
    
    return redirect(url_for('admin.admin_profile'))

@admin.route("/admin/register", methods=["POST"])
@roles_accepted('Admin')
def admin_register():
    # search user in database
    user = User.query.filter_by(email=request.form['email']).first()

    if user:
        flash('Email existed.')
        return redirect(url_for("admin.admin_profile"))
    
    #find the role
    role = Role.query.filter_by(name="Admin").first()

    # store the user to database
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    birthdate = request.form.get("birthdate").split("-")
    user = User(email=email, password=generate_password_hash(password, method='scrypt'), name=name, active=1, birthdate=datetime(int(birthdate[0]),int(birthdate[1]),int(birthdate[2])))
    
    user.roles.append(role)
        
    # commit the changes to database
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("admin.admin_profile"))

@admin.route("/admin/profile")
@roles_accepted('Admin')
def admin_profile():
    admin_list = User.query.all()
    foods = Food.query.all()
    return render_template("admin_profile.html", user = current_user, admins=admin_list, foods=foods)

@admin.route("/admin/foodinsertion", methods=["POST"])
@roles_accepted('Admin')
def add_food():
    name = request.form.get("name")
    calo = request.form.get("calo")
    food = Food(name=name, calo=calo)

    # commit the change
    db.session.add(food)
    db.session.commit()
    return redirect(url_for("admin.admin_profile"))

@admin.route("/admin/logout")
def admin_logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("admin.admin_login"))