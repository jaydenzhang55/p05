'''
Jayden Zhang, Margie Cao, Danny Huang, Kyle Lee
404NotFound
SoftDev
P04
Time spent: tbd
Target Ship Date: 2025-06-06
'''

import os
import db as db
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for

import pikepdf
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

##image configuration
upload_folder = 'static/images'
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config['upload_folder'] = upload_folder

##image configuration
upload_folder = 'static/images'
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config['upload_folder'] = upload_folder

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
    if signed_in():
        return render_template("index.html", loggedIn=True, username=session['username'])
    else:
        return render_template("index.html", loggedIn=False, username='None')

@app.route('/login', methods=['GET', 'POST'])
def login():
     if signed_in():
        return redirect('/')
     elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pw')
        if not check_user(username):
            return render_template("login.html", message="No such username exists", loggedIn=True)
        if not check_password(username, password):
            return render_template("login.html", message="Incorrect password", loggedIn=False)
        session['username'] = username
        session["password"] = request.form.get("pw")
        return redirect('/')
     return render_template("login.html", loggedIn=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if signed_in():
        return redirect('/')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['pw']     
        user = db.getUser(username)
        if user is None:
            db.addUser(username, password)
            session["username"] = username
            session["password"] = password
            return redirect('/login')
        else:
            return render_template('register.html', message="Username already exists", loggedIn=False)
    return render_template("register.html", loggedIn=False)

@app.route('/saved/<username>', methods=['GET', 'POST'])
def saved(username):
    if signed_in():
        return render_template("saved.html", loggedIn=True, username=session['username'])
    else:
        return render_template("saved.html", loggedIn=False)

@app.route('/book/<ISBN>', methods=['GET', 'POST'])
def book(ISBN):
    if signed_in():
        return render_template("book.html", loggedIn=True, username=session['username'])
    else:
        return render_template("book.html", loggedIn=False)
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        search = request.form.get('search')
        if signed_in():
            return render_template("search.html", loggedIn=True, search=search, username=session['username'])
        else:
            return render_template("search.html", loggedIn=False, search=search)
    
@app.route('/logout', methods=['GET', 'POST'])
def logOut():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')
    
def compress_pdf_pikepdf(input_path, output_path):
    with pikepdf.open(input_path) as pdf:
        pdf.save(output_path, optimize_version=True, compression=pikepdf.CompressionLevel.compression_default)

#compress_pdf_pikepdf("input.pdf", "compressed.pdf")

def websiteLinkCreator(query):
    queryArray = query.split(' ')
    modification = ""
    for _ in range(len(queryArray)):
        modification = queryArray[_]
    URL = "https://annas-archive.org/search?q=" + modification
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all('a'):
        print(link.get('href'))

    return soup.find_all('a')

def getDownloadPDFLink(chosenLink): 
    URL = "https://annas-archive.org" + chosenLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    listOfLinks = []

    for link in soup.find_all('a'):
        if "slow" in link:
            listOfLinks.append(link)

    return listOfLinks

def download_pdf_file(download_url, output_path):
    response = requests.get(download_url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

def PDF(chosenLink, query):
    listOfLinks = getDownloadPDFLink(chosenLink)
    originalPath = "downloaded.pdf"
    compressedPath = "compressed.pdf"
    download_pdf_file("https://annas-archive.org" + listOfLinks[0], originalPath)
    compress_pdf_pikepdf(originalPath, compressedPath)
    db.storePDF(query, compressedPath)

    os.remove(originalPath)
    os.remove(compressedPath)


if __name__ == "__main__":
#     app.debug = False
#     app.run(host='0.0.0.0')
    app.debug = True
    app.run(host='127.0.0.1')
    

 


