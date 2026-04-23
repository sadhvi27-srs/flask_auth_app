# Flask Auth App (MySQL)

A login/signup web app built with Flask and MySQL, using bcrypt for password hashing.

---

## Project Structure

```
flask_auth_app/
├── app.py
├── requirements.txt
└── templates/
    ├── login.html
    ├── signup.html
    └── dashboard.html
```

---

## Setup Instructions

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Configure MySQL credentials
Open `app.py` and update the `DB_CONFIG` section:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # your MySQL username
    'password': 'password',  # your MySQL password
    'database': 'auth_app'
}
```

### 3. Run the app
```bash
python app.py
```
The app auto-creates the `auth_app` database and tables on first run,
and inserts 3 dummy users.

### 4. Open in browser
```
http://localhost:5000
```

---

## Dummy Accounts (pre-loaded)

| Name           | Email                 | Mobile      | Password     |
|----------------|-----------------------|-------------|--------------|
| Alice Johnson  | alice@example.com     | 9876543210  | Alice@123    |
| Bob Smith      | bob@example.com       | 9876543211  | Bob@123      |
| Charlie Brown  | charlie@example.com   | 9876543212  | Charlie@123  |

---

## Features
- Sign up with name + email and/or mobile
- Login using email **or** mobile number
- Passwords stored as bcrypt hashes (never plain text)
- MySQL database (auto-created on first run)
- Session-based authentication
- Flash messages for errors and success
- Clean dark UI
