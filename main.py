from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, current_user
from flask_security import roles_accepted
from app import app
from datetime import date
from models import *

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html", current_user = current_user)

@main.route("/profile")
@roles_accepted("User")
def profile():
    foods = Food.query.all()
    latest_weight = UserWeight.query.filter_by(userId=current_user.id).order_by(UserWeight.date_created.desc()).first()
    latest_height = UserHeight.query.filter_by(userId=current_user.id).order_by(UserHeight.date_created.desc()).first()
    age = calculate_age(current_user.birthdate)

    #Man: BMR = 10W + 6.25H + -5A + 5, Woman: BMR = 10W + 6.25H + -5A - 161
    tdee = None
    if latest_height and latest_weight:
        if current_user.gender == True:
            bmr = 10 * int(latest_weight.weight) + 6.25 * int(latest_height.height) - 5 * age + 5
        else:
            bmr = 10 * int(latest_weight.weight) + 6.25 * int(latest_height.height) - 5 * age - 161
        tdee = round(bmr * 1.55)


    return render_template("profile.html",current_user = current_user, foods=foods, weight=latest_weight, height=latest_height, age=age, tdee=tdee)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@main.route("/profile", methods=["POST"])
@roles_accepted("User")
def profile_post():
    #height insertion
    height = request.form.get("height")
    if height:
        latest_height = UserHeight.query.filter_by(userId=current_user.id).order_by(UserHeight.date_created.desc()).first()
        recId = 1
        if latest_height:
            recId = latest_height.recId + 1
        userHeight = UserHeight(userId = current_user.id, recId=recId, height = height)
        db.session.add(userHeight)

    #weight insertion
    weight = request.form.get("weight")
    if weight:
        latest_weight = UserWeight.query.filter_by(userId=current_user.id).order_by(UserWeight.date_created.desc()).first()
        recId = 1
        if latest_weight:
            recId = latest_weight.recId + 1
        userWeight = UserWeight(userId = current_user.id, recId=recId, weight = weight)
        db.session.add(userWeight)

    db.session.commit()

    return redirect(url_for('main.profile'))