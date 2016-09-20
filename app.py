from flask import Flask, request, render_template
import sqlite3
from sqlite3 import OperationalError
import json
import short_url


# Declare app variable
app = Flask(__name__)

# String of characters referened for encoding and decoding
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

test = decode_base62('3e')
print test

def table_schema():
	# Create url_data table in SQL
	with sqlite3.connect('url.db') as db:
		cursor = db.cursor()
		table_creation = """
			CREATE TABLE url_data(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			shortened_url text,
			actual_url text,
			num_redirects text,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
			"""
		try:
			cursor.execute(table_creation)
		except OperationalError:
			pass

# Routing for adding a new url to the database
@app.route('/', methods=['POST', 'GET'])
def homepage():
	if request.method == 'POST':
		# actual_url = request.form.get('actual_url')
		actual_url = request.json['actual_url']
		print '!!!!!!!????', actual_url
		with sqlite3.connect('url.db') as db:
			cursor = db.cursor()
			save_url = """
				INSERT INTO url_data (actual_url, num_redirects)
				VALUES ('%(actual_url)s', '%(num_redirects)s')
			"""%{'actual_url': actual_url, 'num_redirects': 0}
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
	return render_template('index.html')

@app.route('/links', methods=['POST', 'GET'])
def linkspage():
	if request.method == 'GET':
		with sqlite3.connect('url.db') as db:
			cursor = db.cursor()
			query = ('SELECT * FROM url_data')
			cursor.execute(query)
			return json.dumps(repr(cursor.fetchall()))

if __name__ == "__main__":
	table_schema()
	app.run(debug=True)
