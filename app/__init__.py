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
    return 'Project 5'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')