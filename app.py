import flask
from flask import Flask, redirect, request, render_template, Response
import sqlite3
from sqlite3 import OperationalError

# Declare app variable
app = Flask(__name__)
app.config.from_object(__name__)

# String of characters referenced for encoding and decoding
base_62_alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Function to encode string using base 62 methodology
def encode_base62(num, alphabet=base_62_alphabet):
	if num == 0:
		return alphabet[0]
	result = []
	base = len(alphabet)
	while num:
		num, rem = divmod(num, base)
		result.append(alphabet[rem])
	result.reverse()
	return ''.join(result)

# Function to decode a string to original string
def decode_base62(string, alphabet=base_62_alphabet):
	base = len(alphabet)
	string_length = len(string)
	num = 0
	index = 0
	for i in string:
		power = (string_length - (index + 1))
		num += alphabet.index(i) * (base ** power)
		index += 1
	return num

# Define database file
database_name = 'url.db'
def update_database(new_db_name):
	database_name = new_db_name

# Function to create url_data table in SQL
def table_schema():
	with sqlite3.connect(database_name) as db:
		cursor = db.cursor()
		table_creation = """
			CREATE TABLE url_data(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			shortened_url text,
			desktop_url text,
			mobile_url text,
			tablet_url text,
			num_redirects integer,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
			"""
		# Create table if not already created
		try:
			cursor.execute(table_creation)
		except OperationalError:
			pass

# Routing for adding a new url to the database
@app.route('/', methods=['POST', 'GET'])
def homepage():
	if request.method == 'POST':
		# Parse out the original urls sent from the client
		desktop_url = request.json['desktop_url']
		mobile_url = request.json['mobile_url']
		tablet_url = request.json['tablet_url']
		with sqlite3.connect(database_name) as db:
			cursor = db.cursor()
			# Query for saving new url to the database
			save_url = """
				INSERT INTO url_data (desktop_url, mobile_url, tablet_url, num_redirects)
				VALUES ('%(desktop_url)s', '%(mobile_url)s', '%(tablet_url)s', '%(num_redirects)s')
			"""%{'desktop_url': desktop_url, 'mobile_url': mobile_url, 'tablet_url': tablet_url, 'num_redirects': 0}
			# Execute the query to add the new url to the database
			execute_cursor = cursor.execute(save_url)
			# Get the id of the new entry and encode it with base62 methodology
			current_id = execute_cursor.lastrowid
			shortened_url = encode_base62(current_id)
			# Save the encoded ID to the shortened_url column
			cursor.execute("""
				UPDATE url_data SET shortened_url='%(shortened_url)s'
				WHERE ID='%(current_id)s'
			"""%{'shortened_url': shortened_url, 'current_id': current_id})
			# Send response with the information on the updated row
			return flask.jsonify(**{'current_id': current_id, 'shortened_url': shortened_url})
	return render_template('index.html')

# Request to get full list of URL data in SQL
@app.route('/links', methods=['POST', 'GET'])
def links():
	if request.method == 'GET':
		with sqlite3.connect(database_name) as db:
			db.text_factory = str
			cursor = db.cursor()
			# Select all data from the table
			entire_db = cursor.execute('SELECT * FROM url_data')
			# Convert the results from a list to a dictionary...
			# ... so that it can be stringified properly with flask.jsonify
			db_dict = {}
			for row in entire_db:
				db_dict[row[1]] = row
			print db_dict
			return flask.jsonify(**db_dict)

# Redirect to actual url using Flask dynamic routing
@app.route('/<encoded_url>')
def actual_url_redirect(encoded_url):
    with sqlite3.connect(database_name) as db:
	    device = request.args.get('device')
	    # Decode the shortened url into the original ID
	    decoded_url = decode_base62(encoded_url)
	    cursor = db.cursor()
	    db.text_factory = str
	    # Query to select the row that corresponds to the decoded ID
	    # Query for desktop
	    desktop_url = """
	      SELECT desktop_url FROM url_data
	        WHERE id=%s
	      """%(decoded_url)
	    # Query for mobile
	    mobile_url = """
	      SELECT mobile_url FROM url_data
	        WHERE id=%s
	      """%(decoded_url)
	    # Query for tablet
	    tablet_url = """
	      SELECT tablet_url FROM url_data
	        WHERE id=%s
	      """%(decoded_url)	   	
	    # Row has been selected, now we want to find the original url for redirection
	    # Make selection based on the device type
	    if (device == 'desktop'):
		   	# Increment the redirect count in SQL for that url
	    	cursor.execute("""UPDATE url_data SET num_redirects=num_redirects+1 WHERE id=%s"""%(decoded_url))
	     	# Redirect to the desktop url
	     	return redirect(cursor.execute(desktop_url).fetchone()[0])
	    if (device == 'mobile'):
	    	# Increment the redirect count in SQL for that url
	    	cursor.execute("""UPDATE url_data SET num_redirects=num_redirects+1 WHERE id=%s"""%(decoded_url))
	    	# Redirect to the mobile url
	     	return redirect(cursor.execute(mobile_url).fetchone()[0])
	    if (device == 'tablet'):
	    	# Increment the redirect count in SQL for that url
	    	cursor.execute("""UPDATE url_data SET num_redirects=num_redirects+1 WHERE id=%s"""%(decoded_url))
	    	# Redirect to the tablet url
	     	return redirect(cursor.execute(tablet_url).fetchone()[0])


if __name__ == "__main__":
	# Execute url_data table creation in database
	table_schema()
	# Running app in debug mode for development
	app.run(debug=True)
