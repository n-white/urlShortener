# Url Shortener

Please install the below dependencies:
- flask
- sqlite3
- Note: this application was created using Python 2.7

How to start this application:
- `python app.py` from the main folder
- The application will run on localhost at port 5000

API directions
To make a POST request for adding a new URL, please send the following data in a JSON object to "http://localhost:5000/":
- "desktop_url", "mobile_url", "tablet_url"
- After a post request is made, the server will respond with the shortened URL
- Example of a curl request for a URL to GitHub:
	- curl -X POST -H "Content-Type: application/json" -d '{"desktop_url":"http://www.github.com","mobile_url":"http://www.github.com","tablet_url":"http://www.github.com"}' "http://localhost:5000/"

To navigate to the shortened URL, please navigate to the following in your browser:
- http://localhost:5000/<shortened_url>?device=<device_type>
- Note:
- shortened_url will be the shortened_url that was sent back from a post request to "/"
- The query string with device_type can either be set to "desktop", "mobile" or "tablet"

To obtain a list of all URLs in the database, send a GET request to "http://localhost:5000/links"
- The response will conatain the following for each row: shortened_url, desktop_url, mobile_url, tablet_url, num_redirects, created_at

How to run the tests on application:
-  `python app_tests.py` from the main folder