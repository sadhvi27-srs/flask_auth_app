from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ─────────────────────────────
# MySQL CONFIG (FIXED)
# ─────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'appuser',
    'password': 'password123',
    'database': 'user_auth'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ─────────────────────────────
# INIT DATABASE (run once safe)
# ─────────────────────────────
def init_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS user_auth")
    cursor.execute("USE user_auth")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            mobile VARCHAR(15),
            password VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ─────────────────────────────
# HOME
# ─────────────────────────────
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# ─────────────────────────────
# SIGNUP
# ─────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form.get('email')
        mobile   = request.form.get('mobile')
        password = request.form['password']
        confirm  = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (name, email, mobile, password)
                VALUES (%s, %s, %s, %s)
            """, (name, email, mobile, hashed_password.decode('utf-8')))

            conn.commit()
            flash("Signup successful! Please login", "success")
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')

# ─────────────────────────────
# LOGIN
# ─────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password   = request.form['password']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM users
            WHERE email=%s OR mobile=%s
        """, (identifier, identifier))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

# ─────────────────────────────
# DASHBOARD
# ─────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['user_name'])

# ─────────────────────────────
# LOGOUT
# ─────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─────────────────────────────
# RUN APP (IMPORTANT FIX)
# ─────────────────────────────
if __name__ == '__main__':
    # run only first time if needed
    # init_db()

    app.run(host='0.0.0.0', port=5000, debug=True)
