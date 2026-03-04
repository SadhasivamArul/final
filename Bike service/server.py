from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# -------- SQL SERVER CONNECTION --------
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-VFBMD49\\SQLEXPRESS;"
    "Database=OmegaBikeService;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

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

    # Confirm password check
    if password != repassword:
        return "❌ Password and Confirm Password do not match!"

    # Check if user already exists
    cursor.execute(
        "SELECT * FROM Users WHERE username=? OR phone=? OR email=?",
        (username, phone, email)
    )
    existing_user = cursor.fetchone()

    if existing_user:
        return "❌ Username / Phone / Email already exists!"

    # Insert new user
    cursor.execute(
        "INSERT INTO Users (username, phone, email, password) VALUES (?, ?, ?, ?)",
        (username, phone, email, password)
    )
    conn.commit()

    return redirect('/signin')

# -------- LOGIN --------
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    # Step 1: Check if username exists
    cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:
        return "❌ Account does not exist. Please Sign Up."

    # Step 2: Check password
    cursor.execute(
        "SELECT * FROM Users WHERE username=? AND password=?",
        (username, password)
    )
    valid_user = cursor.fetchone()

    if valid_user:
        return "✅ Login Successful!"
    else:
        return "❌ Wrong Password!"

# -------- RUN SERVER --------
if __name__ == '__main__':
    app.run(debug=True)