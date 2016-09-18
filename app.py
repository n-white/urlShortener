from flask import Flask, request, render_template
import sqlite3
from sqlite3 import OperationalError
import json

# Declare app variable
app = Flask(__name__)

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

@app.route('/', methods=['POST', 'GET'])
def homepage():
	actual_url = request.form.get('actual_url')
	if request.method == 'POST':
		with sqlite3.connect('url.db') as db:
			cursor = db.cursor()
			query = """
				INSERT INTO url_data (shortened_url)
				VALUES ('%s')
			"""%(actual_url)
			result_cursor = cursor.execute(query)
	if request.method == 'GET':
		with sqlite3.connect('url.db') as db:
			cursor = db.cursor()
			query = ('SELECT * FROM url_data')
			cursor.execute(query)
			return json.dumps(repr(cursor.fetchall()))
	return render_template('index.html')




if __name__ == "__main__":
	table_schema()
	app.run()
