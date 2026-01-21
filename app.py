#!/usr/bin/python3
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(32)

def init_db():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def check_account(username, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('select * from accounts where username = ? and password = ?',
    (username,password))
    user = cursor.fetchone()
    conn.close()
    return user

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
    if check_account(username, password):
        session['username'] = username
        return redirect(url_for('get_login_success'))
    else:
        return redirect(url_for('get_login_fail'))


@app.route('/login_success')
def get_login_success():
    if 'username' not in session:
        return redirect(url_for('get_login'))
    return render_template('login_success.html')


@app.route('/login_fail')
def get_login_fail():
    if 'username' in session:
        return redirect(url_for('get_login_success'))
    return render_template('login_fail.html')

@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect(url_for('get_login'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)