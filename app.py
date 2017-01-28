import os
from flask import Flask, request, render_template, url_for, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,AnonymousUserMixin

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)

class Journal(db.Model):
	__tablename__ = 'journal'
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String, nullable = False)
	journal_text = db.Column(db.String, nullable = False)
	link = db.Column(db.String, nullable = False)

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	firstname = db.Column(db.String(50),nullable = True)
	lastname = db.Column(db.String(50),nullable = True)
	email = db.Column(db.String(50),nullable = True)
	username = db.Column(db.String(64),nullable = True)
	password = db.Column(db.String(100),nullable = True)
	password_hash = db.Column(db.String(128), nullable = True)

@app.route('/')
def index():
	journals = Journal.query.all()
	return render_template('index.html', journals = journals)

@app.route('/formpost', methods = ["GET", "POST"])
def formpost():
	journal_title = request.form["journaltitle"]
	journal_text = request.form["synopsis"]

	journal = Journal( title = journal_title, journal_text = journal_text)
	db.session.add(journal)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/create_paper', methods = ["GET", "POST"])
def create_paper():
	if request.method == "GET":
		return render_template('create_journal.html')
	if request.method == "POST":
		print 'post'
		journal_title = request.form["journaltitle"]
		journal_text = request.form["synopsis"]
		link = request.form["link"]
		print journal_title

		journal = Journal( title = journal_title, journal_text = journal_text, link = link)
		db.session.add(journal)
		db.session.commit()
		return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug = True)