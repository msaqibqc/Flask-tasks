Flask-tasks
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

	$ virtualenv venv
	$ source venv/bin/activate
	(venv) $ pip install -r requirements.txt
If you are on Windows, then use the following commands instead:

	$ virtualenv venv
	$ venv\Scripts\activate
	(venv) $ pip install -r requirements.txt

API DOCUMENTATION:

- GET /api/users/<int:id>
	To get the user on the base of id

- GET /api/token
	To get the authenticated token

- GET /api/resource To get the resource



Running

To run the server use the following command:

	(venv) $ python app.py
 	* Running on http://127.0.0.1:5000/
 	* Restarting with reloader
Then from a different terminal window you can send requests.

But to authenticate it user must have to run the following commands first to add the user to the db for authentication.

Example

The following curl command registers a new user with username miguel and password python:

$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"miguel","password":"python"}' http://127.0.0.1:5000/api/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 27
Location: http://127.0.0.1:5000/api/users/1
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 19:56:39 GMT

{
  "username": "miguel"
}


These credentials can now be used to access protected resources:

$ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 30
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:02:25 GMT

{
  "data": "Hello, miguel!"
}


Using the wrong credentials the request is refused:

$ curl -u miguel:ruby -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:03:18 GMT

Unauthorized Access


Finally, to avoid sending username and password with every request an authentication token can be requested:

$ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 139
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:04:15 GMT

{
  "duration": 600,
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc"
}


And now during the token validity period there is no need to send username and password to authenticate anymore:

$ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:x -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 30
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:05:08 GMT

{
  "data": "Hello, miguel!"
}