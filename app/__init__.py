'''
Jayden Zhang, Margie Cao, Danny Huang, Kyle Lee
404NotFound
SoftDev
P04
Time spent: tbd
Target Ship Date: 2025-06-06
'''


import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

def signed_in():
    return 'username' in session.keys() and session['username'] is not None

def check_user(username):
    user = db.getUser(username)
    print(user)
    if user is None:
        return False
    return user[0] == username

def check_password(username, password):
    user = db.getHash(username)
    if user is None:
        return False
    print(user)
    return user[0] == password

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
     if signed_in():
        return redirect('/')
     elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pw')
        if not check_user(username):
            return render_template("signIn.html", message="No such username exists")
        if not check_password(username, password):
            return render_template("signIn.html", message="Incorrect password")
        session['username'] = username
        session["password"] = request.form.get("pw")
        return redirect('/')
     return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if signed_in():
        return redirect('/')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['pw']     
        user = db.getUser(username)
        if user is None:
            db.addUser(name, username, password)
            session["username"] = username
            session["password"] = password
            return redirect('/login')
        else:
            return render_template('register.html', message="Username already exists")
    return render_template("register.html")

@app.route('/saved/<username>', methods=['GET', 'POST'])
def saved(username):
    return render_template("saved.html")

@app.route('/book/<ISBN>', methods=['GET', 'POST'])
def book(ISBN):
    return render_template("book.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("search.html")

if __name__ == "__main__":
#     app.debug = False
#     app.run(host='0.0.0.0')
    app.debug = True
    app.run(host='127.0.0.1')
    