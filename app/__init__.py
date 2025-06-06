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
import db as db 
from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import Solutions as sol
import pikepdf
import requests
from bs4 import BeautifulSoup
import json
import tempfile
import shutil

app = Flask(__name__)
secret = os.urandom(32)
app.secret_key = secret

def signed_in():
    return 'username' in session.keys() and session['username'] is not None

def check_user(username):
    user = db.getUser(username)
    if user is None:
        return False
    return user[0] == username

def check_password(username, password):
    user = db.getHash(username)
    if user is None:
        return False
    return user[0] == password

@app.route('/', methods=['GET', 'POST'])
def main():
    all = db.getAllPDFs()
    if signed_in():
        if request.method == "POST":
            userRequest = request.form.get('request')
            try:
                websiteLinks = websiteLinkCreator(userRequest)
                print(websiteLinks)
            except Exception as e:
                print(e)

            found = False

            for link in websiteLinks:
                try:
                    downloadLinks = getDownloadPDFLink(link)
                    for link in downloadLinks:
                        if PDF(link, userRequest):
                            found = True
                            break
                    if found: 
                        break
                except Exception as e:
                    print(e)

            if not found:
                flash('Scraping file unsuccessful.', 'error')
            else:
                flash('File scraped successfully!', 'success')
        return render_template("index.html", loggedIn=True, username=session['username'], all=all)
    else:
        if request.method == "POST":
            flash("You must be signed in to request.", 'error')
        return render_template("index.html", loggedIn=False, username=None, all=all)

@app.route('/login', methods=['GET', 'POST'])
def login():
     all = db.getAllPDFs()
     if signed_in():
        return redirect('/')
     elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pw')
        if not check_user(username):
            flash("No such username exists!", 'error')
            return render_template("login.html", loggedIn=False, all=all)
        if not check_password(username, password):
            flash("Incorrect password!", 'error')
            return render_template("login.html", loggedIn=False, all=all)
        session['username'] = username
        session["password"] = request.form.get("pw")
        return redirect('/')
     return render_template("login.html", loggedIn=False, all=all)


@app.route('/register', methods=['GET', 'POST'])
def register():
    all = db.getAllPDFs()
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
            flash("Successfully created account!", 'success')
            return redirect('/login')
        else:
            flash("Username already exists!", 'error')
            return render_template('register.html', loggedIn=False, all=all)
    return render_template("register.html", loggedIn=False, all=all)

@app.route('/saved', methods=['GET', 'POST'])
def save():
    if signed_in():
        return redirect(url_for('saved', username=session['username'])) 
    else: 
        flash("You must be signed in to view saved items.")
        return redirect(url_for('login'))
    
@app.route('/saved/<username>', methods=['GET', 'POST'])
def saved(username):
    if signed_in():
        all = db.getAllPDFs()
        save = db.getSaved(username)
        return render_template("saved.html", loggedIn=True, username=session['username'], saves=save, all=all)
    else:
        flash("You must be signed in to view saved items.")
        return redirect(url_for('login'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    all = db.getAllPDFs()
    title = request.form.get("title")
    pdf_data = None
    pdf_b64 = ""
    save = request.form.get('save')
    print(save)
    if title:
        result = db.searchForPDFData(title)
        if result:
            pdf_data = result[0]
            pdf_b64 = base64.b64encode(pdf_data).decode('utf-8')
    if save is not None:
        if save =="true":
            saved = True
            username = session["username"]
            db.addSave(username, title)
        else:
            saved = False
            username = session["username"]
            db.removeSave(username, title)
    else:
        if not signed_in():
            saved = False
        else:
            alreadySaved = db.getSaved(session['username'])
            if title in alreadySaved:
                saved = True
            else:
                saved = False

    video = None
    explanation = None
    prompt = ""
    if request.method == "POST":
        api_key = getAIKey()
        prompt = request.form.get("prompt", "")
        uploaded_file = request.files.get("file")
        if api_key and prompt:
            explanation = sol.getGeminiExplaination(api_key, prompt)
            video = sol.getGeminiVideo(api_key, prompt)
        elif api_key and uploaded_file:
            explanation = sol.getGeminiVideo(api_key, uploaded_file)

    if not signed_in():
        return render_template("book.html", loggedIn=False, username='', title=title, pdf_b64=pdf_b64, all=all, explanation=explanation, prompt=prompt, video=video, saved = saved)
    else:
        return render_template("book.html", username=session.get('username'), loggedIn=True, title=title, pdf_b64=pdf_b64, all=all, explanation=explanation, prompt=prompt, video=video, saved = saved)
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    all = db.getAllPDFs()
    
    if request.method == 'POST':
        search_term = request.form.get('search', '')
        show_all = request.form.get('showAll', 'false') == 'true'
        sort_type = request.form.get('sort', 'default')
        
        matched_pdfs = db.searchForPDF(search_term)
        
        boolean = False
        lists = []
        
        if matched_pdfs:
            lists = matched_pdfs
            boolean = True
        
        if show_all:
            current_list = all.copy()  
        else:
            current_list = lists.copy()  
        
        if sort_type == 'alphabetical':
            current_list = sorted(current_list, key=str.lower)
        elif sort_type == 'reverse-alphabetical':
            current_list = sorted(current_list, key=str.lower, reverse=True)
        elif sort_type == 'length-short':
            current_list = sorted(current_list, key=len)
        elif sort_type == 'length-long':
            current_list = sorted(current_list, key=len, reverse=True)
        
        if signed_in():
            return render_template(
                "search.html", loggedIn=True, search=search_term, searchFound=boolean, list=current_list, boolean=boolean, username=session["username"], allPdfs=all, showAll=show_all, sort=sort_type  
            )
        else:
            return render_template(
                "search.html",loggedIn=False, search=search_term, searchFound=boolean, list=current_list, boolean=boolean, username=None, allPdfs=all, showAll=show_all, sort=sort_type  
            )
        

@app.route('/logout', methods=['GET', 'POST'])
def logOut():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    all = db.getAllPDFs()
    if signed_in():
        if request.method == 'POST':
            title = request.form.get('title')
            pdf = request.files.get('pdf')
            pdfdata = pdf.read()
            try:
                db.storePDF(title, None, pdfdata)
                flash("Upload successful!", "success")
            except Exception as e:
                flash(str(e), "error")
            return render_template("upload.html", loggedIn=True, username=session['username'], all=all)
        return render_template("upload.html", loggedIn=True, username=session['username'], all=all)
    else: 
        flash("You must be signed in to upload items.")
        return redirect(url_for('login'))

#---------------------------Failed--------------------------------

# def websiteLinkCreator(query):
#     queryArray = query.split(' ')
#     modification = ""
#     for _ in range(len(queryArray)):
#         if "'" in queryArray[_]:
#             queryArray[_].replace("'", "%27")
#         modification = modification + queryArray[_] + "+"

#     modification = modification[:-1]

#     print("modification: " + modification)
#     URL = "https://archive.org/search?query=" + modification
#     page = requests.get(URL)
#     print("URL: " + URL)
#     soup = BeautifulSoup(page.content, "html.parser")

#     # try:
#     #     for link in soup.find_all('a'):
#     #         print(link.get('href'))
#     #     return soup.find_all('a')
#     # except:
#     #     raise Exception("no books found")
#     print(page.text)

#     links = []
#     try:
#         print(soup.find_all('a'))
#         for link in soup.find_all('a', href=True):
#             print("LINK: " + link)
#             href = link['href']
#             if href.startswith('/details/'):
#                 links.append(href)
#         return links
#     except Exception as e:
#         raise Exception("no books found")

def websiteLinkCreator(query):
    """
    Uses Archive.org's official API to search for items
    Returns list of archive.org detail page URLs
    """
    try:
        query = query.strip()
        
        # Parameters:
        # - q: search query
        # - fl: fields to return (identifier is what we need for URLs)
        # - rows: number of results to return
        # - output: response format
        api_url = f"https://archive.org/advancedsearch.php"
        
        params = {
            'q': f'title:"{query}" AND (subject:textbook OR subject:education) AND collection:(internetarchivebooks OR opensource) AND mediatype:texts',
            'fl': 'identifier,title,creator,date,description',  
            'rows': 5,  
            'output': 'json',
        }
        
        print(f"Searching Archive.org API with query: '{query}'")
        print(f"API URL: {api_url}")
        
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()  
        
        data = response.json()
        
        links = []
        docs = data.get('response', {}).get('docs', [])
        
        print(f"API returned {len(docs)} results")
        
        for doc in docs:
            identifier = doc.get('identifier')
            if identifier:
                detail_url = f"https://archive.org/details/{identifier}"
                links.append(detail_url)
                
                # Optional:
                # title = doc.get('title', 'No title')
                # creator = doc.get('creator', 'Unknown creator')
                # print(f"Found: {title} by {creator} - {detail_url}")
        
        print(f"Total links created: {len(links)}")
        return links
        
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        raise Exception(f"Archive.org API request failed: {e}")
    
    except json.JSONDecodeError as e:
        print(f"Failed to parse API response: {e}")
        raise Exception(f"Failed to parse Archive.org API response: {e}")
    
    except Exception as e:
        print(f"Unexpected error in websiteLinkCreator: {e}")
        raise Exception(f"Search failed: {e}")
    
def getDownloadPDFLink(chosenLink): 
    """
    Extract PDF download links from an Archive.org detail page
    """
    try:
        if chosenLink.startswith('http'):
            URL = chosenLink
        else:
            URL = "https://archive.org" + chosenLink
            
        print(f"Getting PDF links from: {URL}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        listOfLinks = []

        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href.endswith('.pdf') or 'format=pdf' in href.lower():
                if href.startswith('http'):
                    listOfLinks.append(href)
                else:
                    listOfLinks.append(f"https://archive.org{href}")

        if len(listOfLinks) == 0:
            print(f"No PDF links found on {URL}")
            raise Exception("no download links found")
            
        print(f"Found {len(listOfLinks)} PDF download links")
        return listOfLinks
        
    except Exception as e:
        print(f"Error getting PDF links: {e}")
        raise Exception(f"Failed to get PDF download links: {e}")

def download_pdf_file(download_url, output_path):
    """Download PDF file with better error handling"""
    try:
        print(f"Downloading PDF from: {download_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(download_url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not download_url.endswith('.pdf'):
            print(f"Warning: Content type is {content_type}, might not be a PDF")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
        print(f"PDF downloaded successfully to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return False

def compress_pdf_pikepdf(input_path, output_path):
    """Compress PDF using pikepdf"""
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path, linearize=True)
        return True
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return False

def PDF(pdf_link, query):
    """
    Download PDF from direct link, compress it, store in database, then cleanup
    
    Args:
        pdf_link (str): Direct URL to PDF file
        query (str): Search query to store with the PDF
    
    Returns:
        bool: True if successful, False otherwise
    """
    temp_dir = None
    
    try:
        temp_dir = tempfile.mkdtemp(prefix="pdf_download_")
        print(f"Created temp directory: {temp_dir}")
        
        original_path = os.path.join(temp_dir, "downloaded.pdf")
        compressed_path = os.path.join(temp_dir, "compressed.pdf")
        
        if not download_pdf_file(pdf_link, original_path):
            print("Failed to download PDF")
            return False
        
        if not compress_pdf_pikepdf(original_path, compressed_path):
            print("Failed to compress PDF")
            return False
        
        with open(compressed_path, 'rb') as f:
            pdf_data = f.read()
        
        db.storePDF(query, None, pdf_data)
        print(f"Successfully stored PDF in database for query: '{query}'")
        
        return True
        
    except Exception as e:
        print(f"Error in PDF processing: {e}")
        return False
        
    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                print(f"Warning: Could not remove temp directory {temp_dir}: {e}")

#---------------------------Failed--------------------------------

# def getDownloadPDFLink(chosenLink): 
#     URL = "https://archive.org" + chosenLink
#     page = requests.get(URL)

#     soup = BeautifulSoup(page.content, "html.parser")
#     listOfLinks = []

#     for link in soup.find_all('a'):
#         if "pdf" in link:
#             listOfLinks.append(link)

#     if len(listOfLinks) == 0:
#         raise Exception("no download links found")
#     return listOfLinks

# def download_pdf_file(download_url, output_path):
#     response = requests.get(download_url)
#     with open(output_path, 'wb') as f:
#         f.write(response.content)

# def PDF(chosenLink, query):
#     listOfLinks = getDownloadPDFLink(chosenLink)
#     originalPath = "downloaded.pdf"
#     compressedPath = "compressed.pdf"
#     download_pdf_file("https://archive.org" + listOfLinks[0], originalPath)
#     compress_pdf_pikepdf(originalPath, compressedPath)
#     db.storePDF(query, compressedPath, None)

#     os.remove(originalPath)
#     os.remove(compressedPath)

def getAIKey():
    with open("keys/key_AI.txt", "r") as file:
        return file.read().strip()


if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')
    # app.debug = True
    # app.run(host='127.0.0.1')

