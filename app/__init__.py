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

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    app.debug = False
    app.run(host='0.0.0.0')
    #app.debug = True
    #app.run(host='127.0.0.1')
    