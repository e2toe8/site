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

def create_account(username, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    try:
        cursor.execute('insert into accounts (username, password) values (?, ?)', 
        (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def check_account(username, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('select * from accounts where username = ? and password = ?',
    (username,password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def get_index():
    if 'username' in session:
        return redirect(url_for('get_login_success'))
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    return render_template('register.html', username = session['username'])

@app.route('/register', methods=['POST'])
def post_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    username = request.form.get('username')
    password = request.form.get('password')
    if create_account(username, password):
        return redirect(url_for('get_login'))
    else:
        return redirect(url_for('get_register_fail'))

@app.route('/login', methods=['GET'])
def get_login():
    if 'username' in session:
        return redirect(url_for('get_index'))

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def post_login():
    if 'username' in session:
        return redirect(url_for('get_index'))

    username = request.form.get('username')
    password = request.form.get('password')
    if check_account(username, password):
        session['username'] = username
        return redirect(url_for('get_index'))
    else:
        return redirect(url_for('get_login_fail'))

@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect(url_for('get_login'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)