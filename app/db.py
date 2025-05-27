import sqlite3, requests, os
from flask import session
import bcrypt

#Create SQLite Table, creates if not already made
DB_FILE = os.path.join(os.path.dirname(__file__), "../database.db")

db = sqlite3.connect(DB_FILE)
cur = db.cursor()


cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')
db.commit()
db.close()

# User Helpers

def userTable():
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

def pdfTable():
    cur.execute("CREATE TABLE IF NOT EXISTS pdfs (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, pdf_data BLOB)")
    db.commit()

def addUser(username, password):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()

def removeUser(id):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute(f"DELETE FROM users WHERE id='{id}'")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()
    
def validateUser(username, password):
    dbPassword = getHash(username)
    if dbPassword:
        return validatePassword(dbPassword, password)
    return False

def getUser(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        user = cur.execute(f"SELECT username FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        user = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return user

def getId(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        Id =  cur.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        Id = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return Id

def getHash(username):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        Hash = cur.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        Hash = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return Hash

def hashPassword(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(bytes, salt)
    return hashedPassword

def validatePassword(hash, password):
    print("Password: " + password)
    print("Matches Hash: " + str(bcrypt.checkpw(password.encode("utf-8"), hash)))
    return bcrypt.checkpw(password.encode("utf-8"), hash)

def storePDF(title, filePath):
    with open(filePath, 'rb') as file:
        blob_data = file.read()

    cur.execute("INSERT INTO pdfs (title, pdf_data) VALUES (?, ?)", (title, blob_data))
    db.commit()

def searchForPDF(title):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    try:
        pdf = cur.execute(f"SELECT pdf_data FROM pdfs WHERE title='{title}'").>
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        pdf = None
    finally: 
         cur.close()
         db.commit()
         db.close()
    return pdf
