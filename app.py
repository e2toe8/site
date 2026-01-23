#!/usr/bin/python3
from flask import Flask, redirect, render_template, request, session, url_for
import os

from db import init_db, create_account, check_account, get_all_posts, create_post, get_post_by_post_id
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def get_index():
    if 'username' not in session:
        return redirect(url_for('get_login'))
    return render_template('index.html', username = session['username'])

@app.route('/register', methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def post_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    username = request.form.get('username')
    password = request.form.get('password')
    if create_account(username, password):
        return redirect(url_for('get_login'))
    else:
        return render_template('register_fail.html')

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
    user = check_account(username, password)
    if user:
        session['author'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('get_index'))
    else:
        return render_template('login_fail.html')

@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect(url_for('get_login'))

@app.route('/posts', methods=['GET'])
def get_posts():
    if 'username' not in session:
        return redirect(url_for('get_login'))
    posts = get_all_posts()
    return render_template('posts.html', posts = posts)

@app.route('/posts/new', methods=['GET'])
def get_new_post():
    if 'username' not in session:
        return redirect(url_for('get_login'))
    return render_template('posts_new.html')

@app.route('/posts/new', methods=['POST'])
def post_new_post():
    if 'username' not in session:
        return redirect(url_for('get_login'))

    title = request.form.get('title')
    content = request.form.get('content')
    author = session['author']
    create_post(title, content, author)
    return redirect(url_for('get_posts'))

@app.route('/posts/<post_id>', methods=['GET'])
def get_posts_post_id(post_id):
    if 'username' not in session:
        return redirect(url_for('get_login'))

    post = get_post_by_post_id(post_id)
    if post:
        return render_template('post.html', post = post)
    else: 
        return redirect(url_for('get_posts'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)