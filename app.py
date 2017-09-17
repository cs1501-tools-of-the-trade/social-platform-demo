from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
	# TODO: check if user is logged in
	return render_template('index.html')

@app.route("/profile")
def profile():
	return "Profile page"

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/register")
def register():
	return "Registration page"