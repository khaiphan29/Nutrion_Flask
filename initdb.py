from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from datetime import datetime

with app.app_context():
    try:
        # init the role to database
        admin_role = Role(name="Admin")
        user_role = Role(name="User")
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
    except:
        print("failed to init roles or created")
        db.session.rollback()

    try:
        #find the role
        role = Role.query.filter_by(name="Admin").first()

        # store the user to database
        user = User(email="admin@admin", password=generate_password_hash("123123", method='scrypt'), name="admin", active=1, birthdate=datetime(2001,10,30))
        
        user.roles.append(role)
            
        # commit the changes to database
        db.session.add(user)
        db.session.commit()
    except:
        print("failed to init admin or created")
        db.session.rollback()