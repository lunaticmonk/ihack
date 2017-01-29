import os
from flask import Flask, request, render_template, url_for, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,AnonymousUserMixin
from sqlalchemy.sql.expression import func

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
	fc = db.Column(db.Integer, nullable = True, default = 0)
	ti = db.Column(db.Integer, nullable = True, default = 0)
	pf = db.Column(db.Integer, nullable = True, default = 0)

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	firstname = db.Column(db.String(50),nullable = True)
	lastname = db.Column(db.String(50),nullable = True)
	email = db.Column(db.String(50),nullable = True)
	username = db.Column(db.String(64),nullable = True)
	password = db.Column(db.String(100),nullable = True)
	password_hash = db.Column(db.String(128), nullable = True)

@app.route('/', methods = ['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		# logic to check the user from database
		# return redirect(url_for('home'))
		if request.form["enrollment_no"] == "admin" and request.form["enrollment_secret"] == '264637d905':
			return redirect(url_for('home'))
		return redirect(url_for('index'))

@app.route('/dashboard')
def home():
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

@app.route('/upvote')
def upvote():
	journal_id = request.args.get('journal_id')
	print journal_id
	fetcheditem = Journal.query.filter_by(id = journal_id).first()
	print fetcheditem
	if request.args.get('btn') == 'fc':
		print 'Before : ',fetcheditem.fc
		fetcheditem.fc += 1
		print 'After : ',fetcheditem.fc
	if request.args.get('btn') == 'ti':
		fetcheditem.ti += 1
	if request.args.get('btn') == 'pf':
		fetcheditem.pf += 1
	db.session.add(fetcheditem)
	db.session.commit()	
	return redirect(url_for('home'))

@app.route('/create_paper', methods = ["GET", "POST"])
def create_paper():
	if request.method == "GET":
		return render_template('create_paper.html')
	if request.method == "POST":
		print 'post'
		journal_title = request.form["journaltitle"]
		journal_text = request.form["synopsis"]
		link = request.form["link"]
		print journal_title

		journal = Journal( title = journal_title, journal_text = journal_text, link = link)
		db.session.add(journal)
		db.session.commit()
		return redirect(url_for('home'))

@app.route('/profile')
def profile():
	return render_template('profile.html')

if __name__ == '__main__':
	app.run(debug = True)