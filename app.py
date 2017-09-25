from flask import Flask, render_template, g, request, jsonify

import sqlite3

app = Flask(__name__)

### Database stuff ###
def get_db():
	# Get the db connection from the global g dictionary
	# and provide a default value of None if it doesn't exist.
	# This lets us cache (save) the connection value so we don't
	# have to reopen/close the connection again, since we're
	# going to need to interact with the DB often.
	db = getattr(g, '_database', None)
	if db is None:
		# Set the connection in the global if it's not already there
		db = g._database = connect_to_database()
	return db

def connect_to_database():
	# Create a connection to the local sqlite file
	conn = sqlite3.connect('db.sqlite3')

	# Set the row factory to be associative, meaning
	# we can access the columns of a particular row
	# by using the column names, rather than indices
	# in an array. ex. 'author_id' instead of '2'
	# (the 2 is arbitrary here)
	conn.row_factory = sqlite3.Row
	return conn

@app.cli.command('initdb')
def init_db():
	# To initialize we must first create a connection to the db
	db = get_db()

	# Then run the schema.sql file within the database
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())

	# commit the changes
	db.commit()

	print('Initialized the database.')

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
	# Get all rows
    rv = cur.fetchall()

	# Only return the first row if one=True
    return (rv[0] if rv else None) if one else rv

# When the app shuts down, we need to close
# the open connection to the database if it exists.
@app.teardown_appcontext
def close_database(exception):
	if hasattr(g, '_database'):
		g._database.close()

### API ###

# This route tells us that at http://my-site-url.com/api/v1/tweet
# we can send a POST request to create a tweet. The parameters
# are passed encoded in the body.
@app.route('/api/v1/tweet/', methods=['POST'])
def create_tweet():
	error = None
	# Do some basic validation to make sure
	# the values are even there. In the real world
	# we would want to make sure the author_id is valid
	# and that the message isn't too long (140 characters)
	if 'message' not in request.form:
		error = 'You must provide a message.'
	elif 'author_id' not in request.form:
		error = 'You must provide an author ID'
	
	if error:
		# Return an error response with the message
		# if invalid
		return jsonify(
			status='error',
			error=error
		)
	
	# Otherwise grab the database connection and insert
	# the tweet into it.
	db = get_db()

	# The question marks in the string to execute are important
	# because they tell us where to expect user-input. The execute()
	# function within the sqlite3 library automatically escapes any
	# dangerous input that the user may have given us. This will prevent
	# SQL injection attacks.
	db.execute('''insert into tweet (message, author_id) values (?, ?)''', [request.form['message'], request.form['author_id']])
	db.commit()

	# Return a success. In the real world, we may want to return the ID of the
	# newly created item. For this case, though, a success message is enough.
	return jsonify(
		status='success'
	)

# Flask has validation in the routing as well, to make sure
# that the type of the input is as expected. Here, the tweet_id
# must be an integer, and so we can specify int:tweet_id. The
# parameter gets passed to the function.
@app.route('/api/v1/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):

	# A SELECT query with another spot for user input (the tweet id).
	# We put one=True because we only expect one result. This will
	# prevent us from having to access the 0th element of the list we get back.
	# ex. Instead of
	# [
	#	{
	#		'tweet_id': 1,
	#		'message': 'test',
	#		'author_id': 2
	#	}
	# ]
	# 
	# we get just the internal dictionary that we want rather than having to access the 0th 
	# element of that list.

	tweet = query_db('''select * from tweet where tweet_id = ?''', [tweet_id], one=True)

	# no tweet found, meaning tweet == None
	if not tweet:
		return jsonify(
			status='error',
			error='Tweet not found'
			
		)
		
	# Return a JSON response with the tweet information as well as
	# a success status
	return jsonify(
			status='success',
			tweet_id=tweet_id,
			message=tweet['message'],
			author_id=tweet['author_id']
		)

# Use PUT for updating an existing entity
@app.route('/api/v1/tweet/<int:tweet_id>', methods=['PUT'])
def update_tweet(tweet_id):
	# First get the tweet
	tweet = query_db('''select * from tweet where tweet_id = ?''', [tweet_id], one=True)
	if not tweet:
		return jsonify(
			status='error',
			error='Tweet not found'
			
		)
	
	# Set the old values first
	message = tweet['message']
	author_id = tweet['author_id']

	changed = False
	# update them if they changed
	if 'message' in request.form:
		message = request.form['message']
		changed = True
	if 'author_id' in request.form:
		author_id = request.form['author_id']
		changed = True

	# We only need to update the values in the database
	# if any of the values actually changed.
	if changed:
		db = get_db()
		db.execute('''update tweet set message = ?, author_id = ? WHERE tweet_id = ?''', [message, author_id, tweet_id])
		db.commit()
	
	# return a success message
	# along with the updated values
	return jsonify(
			status='success',
			tweet_id=tweet_id,
			message=message,
			author_id=author_id
	)

# DELETE for deleting an entity
@app.route('/api/v1/tweet/<int:tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
	# first get the tweet to make sure it exists
	tweet = query_db('''select * from tweet where tweet_id = ?''', [tweet_id], one=True)
	if not tweet:
		return jsonify(
			status='error',
			error='Tweet not found'
			
		)
	
	# delete the tweet with the given ID
	db = get_db()
	db.execute('''delete from tweet where tweet_id=?''', [tweet_id])
	db.commit()

	# customary to return the ID of the deleted
	# object as well.
	return jsonify(
		status='success',
		tweet_id=tweet_id,
	)

### Pages ###
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
	