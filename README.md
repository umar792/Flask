
# 🧪 Getting Started with Flask – Step-by-Step Guide

This guide walks you through how to build a simple web app using **Flask** (a small and powerful web framework for Python). It’s perfect if you’re just starting out and want to learn by doing.

---

## 📦 What is Flask?

Flask is a lightweight web framework written in Python. It's super easy to use and great for beginners. You can build websites, APIs, dashboards, and more with it.

---

## 🛠️ Requirements

Before starting, make sure you have:

- Python installed (Python 3.7+ recommended)
- A terminal or command prompt
- Basic knowledge of Python

---

## 🚀 Step 1: Create a New Flask Project

### 1.1. Make a Project Folder

```bash
mkdir my-flask-app
cd my-flask-app
```

### 1.2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 1.3. Install Flask

```bash
pip install Flask
```

---

## 📄 Step 2: Create Your Flask App File

Create a file named `app.py` in your project folder:

```python
# app.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"
```

---

## ▶️ Step 3: Run Your Flask App

### 3.1. Tell Flask which file to run:

```bash
export FLASK_APP=app.py      # On Windows: set FLASK_APP=app.py
```

### 3.2. Start the Flask server:

```bash
flask run
```

Now open [http://localhost:5000](http://localhost:5000) in your browser.  
You should see: `Hello, Flask!`

---

## ✍️ Step 4: Adding More Pages (Routes)

You can add more pages like this:

```python
@app.route("/about")
def about():
    return "This is the about page"
```

Now if you visit `/about`, it will show that message.

---

## 🖼️ Step 5: Using HTML Templates

Flask uses Jinja2 for templates. First, make a folder called `templates`:

```
my-flask-app/
│
├── app.py
└── templates/
    └── home.html
```

### `home.html` Example:

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Hello {{ name }}!</h1>
</body>
</html>
```

### Update your route to render it:

```python
from flask import render_template

@app.route("/")
def home():
    return render_template("home.html", name="Flask User")
```

---

## 🧾 Step 6: Handling Forms (POST Requests)

### HTML Form:

```html
<!-- templates/login.html -->
<form method="post">
  Username: <input type="text" name="username"><br>
  <input type="submit" value="Login">
</form>
```

### Flask Route:

```python
from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return f"Welcome, {username}!"
    return render_template("login.html")
```

---

## 🔐 Step 7: Using Sessions (Login Example)

```python
from flask import session

app.secret_key = "your_secret_key"  # required for sessions

@app.route("/set-user")
def set_user():
    session["username"] = "admin"
    return "User set in session!"

@app.route("/get-user")
def get_user():
    return f"Logged in as: {session.get('username')}"
```

---

## 🔚 Step 8: Logging Out

```python
@app.route("/logout")
def logout():
    session.pop("username", None)
    return "Logged out!"
```

---

## 📁 Suggested Project Structure

```
my-flask-app/
│
├── app.py
├── templates/
│   ├── home.html
│   └── login.html
├── static/               # for CSS, JS, images (optional)
│   └── style.css
└── .venv/                # virtual environment (optional)
```

---

## ✅ Tips & Notes

- Every route must return a string or a rendered template.
- Use `{{ variable }}` to print Python variables in HTML.
- Use if statements and loops in templates like this:

```html
{% if user %}
  Hello {{ user }}
{% endif %}
```

---

## 📚 What to Learn Next

- Connect to a database (SQLite, PostgreSQL, etc.)
- Use Flask with SQLAlchemy
- Handle user registration and login properly
- Create APIs using Flask-RESTful
- Deploy your app (Heroku, Render, etc.)

---

> Just build and explore. The more you practice, the better you’ll get. Good luck and happy coding! 🚀