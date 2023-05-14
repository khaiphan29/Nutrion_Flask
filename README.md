# Nutrion app
## Technology
+ Python
+ Flask
+ Flask extensions: Flask-SQlAlchemy, flask-security
## Main feature
+ Support Role base authentication
+ Calculate user TDEE
## Installation
### Python libraries
```
pip install -r requirements.txt
```
### Init migration and database
```
flask db init
flask db migrate -m "first mig"
flask db upgrade
```

### Create admin "admin@admin" with psw "123123"
```
python initdb.py
```