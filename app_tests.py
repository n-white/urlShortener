from app import app

import os
import unittest
import tempfile
import json

# app.update_database('test.db')

class FlaskTestCase(unittest.TestCase):

	# Test that post requests are saved to DB successfully
	def test_post_request(self):
		tester = app.test_client(self)
		response = tester.post('/', data='{"actual_url":"http://www.nothing.com"}', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	# Test that get requests successfully retrieve information
	def test_get_request(self):
		tester = app.test_client(self)
		response = tester.get('/links')
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()