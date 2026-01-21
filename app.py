#!/usr/bin/python3
from flask import Flask, redirect, render_template, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)


accounts = {
    'admin': 'qwe123',
    'guest': 'guest',
    'test': 'test',
}


@app.route('/login', methods=['GET'])
def get_login():
    if 'username' in session:
        return redirect(url_for('get_login_success'))

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    if 'username' in session:
        return redirect(url_for('get_login_success'))

    username = request.form.get('username')
    password = request.form.get('password')
    if username in accounts and accounts[username] == password:
        session['username'] = username
        return redirect(url_for('get_login_success'))
    else:
        return redirect(url_for('get_login_fail'))


@app.route('/login-success')
def get_login_success():
    if 'username' not in session:
        return redirect(url_for('get_login'))
    return render_template('login_success.html')


@app.route('/login-fail')
def get_login_fail():
    if 'username' in session:
        return redirect(url_for('get_login_success'))
    return render_template('login_fail.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)