from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# -------- SUPABASE CONNECTION --------
conn = psycopg2.connect(
    host="db.lrsmronreuoqatikdlbu.supabase.co",          # example: db.abcdxyz.supabase.co
    database="postgres",
    user="postgres",
    password="YOUR_PASSWORD",
    port="5432"
)

cursor = conn.cursor()

# -------- HOME --------
@app.route('/')
def home():
    return render_template("index.html")

# -------- SIGNUP PAGE --------
@app.route('/signup')
def signup():
    return render_template("signup.html")

# -------- SIGNIN PAGE --------
@app.route('/signin')
def signin():
    return render_template("signin.html")

# -------- REGISTER --------
@app.route('/register', methods=['POST'])
def register():

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    gender = request.form['gender']
    mobile = request.form['mobile']
    whatsapp = request.form['whatsapp']
    altmobile = request.form['altmobile']
    email = request.form['email']
    address = request.form['address']
    username = request.form['username']
    password = request.form['password']
    repassword = request.form['repassword']

    if password != repassword:
        return "❌ Password not matching!"

    try:
        cursor.execute("""
            INSERT INTO users 
            (firstname, lastname, gender, mobile, whatsapp, altmobile, email, address, username, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (firstname, lastname, gender, mobile, whatsapp, altmobile, email, address, username, password))

        conn.commit()
    except Exception as e:
        conn.rollback()
        return "❌ Username or Email already exists!"

    return redirect('/signin')

# -------- LOGIN --------
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    if not user:
        return "❌ Account not found. Please Sign Up."

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    valid_user = cursor.fetchone()

    if valid_user:
        return "✅ Login Successful!"
    else:
        return "❌ Wrong Password!"

# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)
