'''
Jayden Zhang, Margie Cao, Danny Huang, Kyle Lee
404NotFound
SoftDev
P04
Time spent: tbd
Target Ship Date: 2025-06-06
'''

import base64
import os
from app import db as db 
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import send_file
from flask import Response
from io import BytesIO
from app import Solutions
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
        return render_template("index.html", loggedIn="true", username=session['username'])
    else:
        return render_template("index.html", loggedIn="false", username='')

@app.route('/login', methods=['GET', 'POST'])
def login():
     if signed_in():
        return redirect('/')
     elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pw')
        if not check_user(username):
            return render_template("login.html", message="No such username exists", loggedIn="false")
        if not check_password(username, password):
            return render_template("login.html", message="Incorrect password", loggedIn="false")
        session['username'] = username
        session["password"] = request.form.get("pw")
        return redirect('/')
     return render_template("login.html", loggedIn="false")

@app.route('/solution', methods=['GET', 'POST'])
def solution():
    if not signed_in():
        return render_template("login.html", message="Not logged in!", loggedIn="false")
    else:
        video = None 
        explaination = None
        prompt = ""
        if request.method == "POST":
            #lowkey idk how to hide API keys
            api_key = "AIzaSyDswIW_77_VcDIbXxi_qB-BD9ifUGETSXQ"
            prompt = request.form.get("prompt", "")
            if api_key and prompt:
                explanation = getGeminiExplaination(api_key, prompt)
                video_count = getGeminiVideo(api_key, prompt)
    
    return render_template("solutions.html", explanation=explanation, prompt=prompt, video=video, loggedIn="true")
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
            return render_template('register.html', message="Username already exists", loggedIn="false")
    return render_template("register.html", loggedIn="false")

@app.route('/saved/<username>', methods=['GET', 'POST'])
def saved(username):
    if signed_in():
        return render_template("saved.html", loggedIn="true", username=session['username'])
    else:
        return render_template("saved.html", loggedIn="false", username='')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if signed_in():
        title = request.form.get("title")
        pdf_data = db.searchForPDFData(title)[0]

        if pdf_data:
            pdf_b64 = base64.b64encode(pdf_data).decode('utf-8')
            return render_template("book.html", loggedIn="true", username=session['username'], title=title, pdf_b64=pdf_b64)
    else:
        return render_template("book.html", loggedIn="false", username='')
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search')

        if signed_in():
            # Try to search for matching PDFs
            matched_pdfs = db.searchForPDF(search_term)
            
            if matched_pdfs:
                # If matches found, show them
                return render_template(
                    "search.html",loggedIn="true",search=search_term,list=matched_pdfs, boolean=True, secondBool=True, username=session["username"]
                )
            else:
                # No matches found, show all PDFs in DB
                all_pdfs = db.getAllPDFs()  
                return render_template(
                    "search.html",loggedIn="true",search=search_term,list=all_pdfs,boolean=False,secondBool=True,username=session["username"]
                )
        else:
            # Not signed in
            return render_template(
                "search.html",loggedIn="false",search=search_term,boolean=False,username=None
            )

    if signed_in():
        all_pdfs = db.getAllPDFs()  
        return render_template(
            "search.html",loggedIn="true",search="",list=all_pdfs,boolean=True,secondBool=False,username=session["username"]
        )
    else:
        return render_template(
            "search.html",loggedIn="false",search="",boolean=False,username=None
        )

    
@app.route('/logout', methods=['GET', 'POST'])
def logOut():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if signed_in():
        if request.method == 'POST':
            title = request.form.get('title')
            pdf = request.files.get('pdf')
            pdfdata = pdf.read()
            db.storePDF(title, None, pdfdata)
            return render_template("upload.html", message = "upload successful", loggedIn="true", username=session['username'])
        return render_template("upload.html", loggedIn="true", username=session['username'])
    return redirect('/login')

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
    db.storePDF(query, compressedPath, None)

    os.remove(originalPath)
    os.remove(compressedPath)


if __name__ == "__main__":
#     app.debug = False
#     app.run(host='0.0.0.0')
    app.debug = True
    app.run(host='127.0.0.1')

