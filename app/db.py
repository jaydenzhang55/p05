import sqlite3, requests, os
from flask import session
import bcrypt
from collections import defaultdict

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
cur.execute("CREATE TABLE IF NOT EXISTS pdfs(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, pdf_data BLOB)")
cur.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content Blob,
            Textbook_id INTEGER,
            FOREIGN KEY(Textbook_id) REFERENCES pdfs(id)
        )

    ''')
db.commit()
db.close()

# User Helpers

def userTable():
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

def pdfTable():
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS pdfs(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, pdf_data BLOB)")
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()

def saveTable():
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS saves(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, pdf_data BLOB)")
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        db.commit()
        db.close()

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

def addSaveIDs(pdfid):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute("INSERT INTO users (saveIDs) VALUES (?)", (pdfid))
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

def storePDF(title, file_path, data):
    maxSize=40 * 1024 * 1024 # 40 mb is max
    with sqlite3.connect(DB_FILE) as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM pdfs WHERE title = ?", (title,))
        if cur.fetchone()[0] > 0:
            raise Exception(f"PDF with title '{title}' already exists.")

        if file_path != None:
            with open(file_path, 'rb') as f:
                blob_data = f.read()
        else:
            blob_data = data

        if len(blob_data) > maxSize:
            raise Exception("File too large")

        cur.execute("INSERT INTO pdfs(title, pdf_data) VALUES (?, ?)", (title, sqlite3.Binary(blob_data)))
        db.commit()

# def searchForPDF(title):
#     db = sqlite3.connect(DB_FILE)
#     cur = db.cursor()
#     try:
#         pdf = cur.execute(f"SELECT pdf_data FROM pdfs WHERE title='{title}'").fetchall()
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         pdf = None
#     finally: 
#          cur.close()
#          db.commit()
#          db.close()
#     return pdf

def stringSplitter(text):
    text = text.lower()
    text2 = ''
    for i in text:
        if i.isalnum() or i.isspace():
            text2 += i
        else:
            text2 += ' '
    return text2.split()

def getAllPDFs():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT title FROM pdfs")  
    results = cur.fetchall()
    db.close()
    return [row[0] for row in results]

def getSaved():
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT title FROM saves")  
    results = cur.fetchall()
    db.close()
    return [row[0] for row in results]

def searchForPDFII(query):
    conn = sqlite3.connect(pdfs.db)
    cursor = conn.cursor()
    invertedIndex = defaultdict(set)
    idTitle = {}
    cursor.execute("SELECT id, title FROM pdfs")
    for pdfID, title in cursor.fetchall():
        idTitle[pdfID] = title
        tokens = set(tokenize(title))
        for token in tokens:
            invertedIndex[token].add(pdfID)
    queryTokens = stringSplitter(query)
    if not queryTokens:
        return []
    result = inverted_index.get(queryTokens[0], set()).copy()
    for token in queryTokens[1:]:
        result &= invertedIndex.get(token, set())
    conn.close()
    return [(pdfID, idTitle[pdfID]) for pdfID in result]

def searchForPDF(keyword):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT title FROM pdfs WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cur.fetchall()
    db.close()
    return [row[0] for row in results]

def searchForPDFData(keyword):
    db = sqlite3.connect(DB_FILE)
    cur = db.cursor()
    cur.execute("SELECT pdf_data FROM pdfs WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cur.fetchall()
    db.close()
    return [row[0] for row in results]

def addQuestion(question, textbook_id):
    try:
        db = sqlite3.connect(DB_FILE)
        cur = db.cursor()
        cur.execute('''
            INSERT INTO questions (content, Textbook_id)  
            VALUES (?, ?)
        ''', (question, textbook_id))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        db.commit()
        cur.close()
        db.close()
#storePDF('Brocks Biology of Microorganisms', "./static/Brock Biology of Microorganisms.pdf", None)
saveTable()
