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

@app.route('/', methods=['GET', 'POST'])
def main():
    return 'Project 5'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

def compress_pdf_pikepdf(input_path, output_path):
    with pikepdf.open(input_path) as pdf:
        pdf.save(output_path, optimize_version=True, compression=pikepdf.CompressionLevel.compression_default)

compress_pdf_pikepdf("input.pdf", "compressed.pdf")

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

def downloadPDF(chosenLink): 
    URL = "https://annas-archive.org" + chosenLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    listOfLinks = []

    for link in soup.find_all('a'):
        if "slow" in link:
            listOfLinks.append(link)

    return listOfLinks

 


