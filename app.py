from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://smqxuzwltqacvh:2c0196e786c746bf0c8ce2636d1f2062a709554c22b29e788ce83d89143f524f@ec2-184-72-239-186.compute-1.amazonaws.com:5432/dbut9mmap3u2jt"
heroku = Heroku(app)
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, email):
		self.email = email

	def __repr__(self):
		return '<E-mail %r>' % self.email


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/collections', methods=['POST'])
def collections():
	email = None
	if request.method == 'POST':
		email = request.form['email']
		if not db.session.query(User).filter(User.email == email).count():
			reg = User(email)
			db.session.add(reg)
			db.session.commit()
			return render_template('success.html')
	return render_template('home.html')

@app.route('/return_emails', methods=['GET'])
def return_emails():
	all_emails = db.session.query(User.email).all()
	return jsonify(all_emails)


if __name__ == '__main__':
	app.debug = True
	app.run()