from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# -------- DATABASE FILE --------
DATABASE = 'OmegaBikeService'

# -------- CREATE TABLE IF NOT EXISTS --------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            phone TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# -------- HOME --------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/client')
def client():
    return render_template("client.html")

# -------- SIGNUP PAGE --------
@app.route('/signup')
def signup():
    return render_template("signup.html")

# -------- SIGNIN PAGE --------
@app.route('/signin')
def signin():
    return render_template("signin.html")

# -------- REGISTER USER --------
@app.route('/register', methods=['POST'])
def register():

    username = request.form['username']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    repassword = request.form['repassword']

    if password != repassword:
        return "❌ Password and Confirm Password do not match!"

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Users (username, phone, email, password) VALUES (?, ?, ?, ?)",
            (username, phone, email, password)
        )
        conn.commit()
    except:
        conn.close()
        return "❌ Username / Phone / Email already exists!"

    conn.close()
    return redirect('/signin')

# -------- LOGIN --------
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if account exists
    cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "❌ Account does not exist. Please Sign Up."

    # Check password
    cursor.execute(
        "SELECT * FROM Users WHERE username=? AND password=?",
        (username, password)
    )
    valid_user = cursor.fetchone()

    conn.close()

    if valid_user:
        return "✅ Login Successful!"
    else:
        return "❌ Wrong Password!"

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)