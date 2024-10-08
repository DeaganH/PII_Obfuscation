import json
import os
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':

    app.run(debug=True)