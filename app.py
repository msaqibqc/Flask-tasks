from flask import request, abort, Flask, render_template, jsonify , g
from flask_httpauth import HTTPBasicAuth
from flaskext.mysql import MySQL
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# Database connectivity
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = "random string"
mysql.init_app(app)


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token

    return 1

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        g.user = data
        return True


def generate_auth_token(expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': id})


@app.route("/")
@auth.login_required
def hello():
    """
    Renders the main page of application
    :return: web_page
    """
    return render_template('login.html')


@app.route('/api/token')
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route("/api/logout")
@auth.login_required
def logout():
    """
    Logout the user from website
    :return: web_page
    """
    # session['logged_in'] = False
    # @auth. = Falselse
    return hello()


@app.route('/api/users', methods=['POST'])
@auth.login_required
def new_user():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return "User is not available in the database"
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()