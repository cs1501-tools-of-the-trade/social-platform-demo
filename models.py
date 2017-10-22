import flask_login

class User(flask_login.UserMixin):
	def __init__(self):
		pass

	def __init__(self, first_name, last_name, username, email):
		self.first_name = first_name
		self.last_name = last_name
		self.username = username
		self.email = email