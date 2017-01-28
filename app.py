import os
from flask import Flask, request, render_template, url_for, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6140009:Y1912zwYwC@sql6.freemysqlhosting.net/sql6140009'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)

class Journal(db.Model):
	__tablename__ = 'journal'
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String, nullable = False)
	journal_text = db.Column(db.String, nullable = False)

@app.route('/')
def index():
	journals = Journal.query.all()
	return render_template('index.html', journals = journals)

@app.route('/formpost', methods = ["GET", "POST"])
def formpost():
	journal_title = request.form["journaltitle"]
	journal_text = request.form["journaltext"]

	journal = Journal( title = journal_title, journal_text = journal_text)
	db.session.add(journal)
	db.session.commit()
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug = True)