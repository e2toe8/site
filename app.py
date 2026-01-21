#!/usr/bin/python3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


accounts = {
    'admin': 'qwe123',
    'guest': 'guest',
    'test': 'test',
}

@app.route('/', methods=['GET'])
def get_home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in accounts and accounts[username] == password:
        return redirect(url_for('get_login_success'))
    else:
        return redirect(url_for('get_login_failure'))


@app.route('/login_success')
def get_login_success():
    return render_template('login_success.html')


@app.route('/login_failure')
def get_login_failure():
    return render_template('login_failure.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)