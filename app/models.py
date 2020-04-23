from app import db

class User(db.Document):
	username = db.StringField(max_length=64, required=True, unique=True)
	email = db.StringField(max_length=120, required=True, unique=True)
	password_hash = db.StringField(max_length=128)

	def __repr__(self):
		return '<User {}>'.format(self.username)