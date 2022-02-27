from enum import unique
from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.views import MethodView



app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def home():
    return "Hello, flask!"


def post():
    return "this is where we post"


def check_health():
    return jsonify({
        "status": "ok"
        })

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(69), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password= db.Column(db.String(123))
    text =  db.Column(db.String(500))

    #def __init__(self, username, email, password):
     ##  self.username =username
       # self.email = email
        #self.password = password

def show_all():
   return render_template('show_all.html', UserModel = UserModel.query.all() )

def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['email'] or not request.form['password']:
            flash('Please enter all the fileds', 'error')
        else:
            UserModell = UserModel(request.form['username'], request.form['email'], request.form['password'], request.form['text'])

            db.session.add(UserModell)
            db.session.commit()
            flash('record was succefully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


app.add_url_rule('/new', view_func=new, methods=['GET', 'POST'])
app.add_url_rule('/', view_func=home, methods=['GET'])
app.add_url_rule('/show', view_func=show_all, methods=['GET'] )
app.add_url_rule('/check_health', view_func=check_health, methods=['GET'])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)