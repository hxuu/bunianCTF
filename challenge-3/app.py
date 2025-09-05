import os
import sqlite3
import jwt
import datetime
from flask import (
    Flask, request, jsonify, g, session,
    redirect, url_for, render_template, render_template_string
)
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------
# Config
# -------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret")
app.config["JWT_SECRET"] = os.environ.get("JWT_SECRET", "fallback_jwt")
FLAG = os.environ.get("FLAG", "Bunian{default_flag}")
DATABASE = "mail.db"


# -------------------------------
# Database Helpers
# -------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    c = db.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            content TEXT NOT NULL
        )"""
    )
    db.commit()
    # Ensure admin user exists
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
              ("admin", generate_password_hash("adminpass")))
    db.commit()


# -------------------------------
# JWT Helpers
# -------------------------------
def create_jwt(username, role="user"):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, app.config["JWT_SECRET"], algorithm="HS256")
    return token


def decode_jwt(token):
    try:
        return jwt.decode(token, app.config["JWT_SECRET"], algorithms=["HS256"])
    except Exception:
        return None


# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
        except sqlite3.IntegrityError:
            return "Username already taken"
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        c = db.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            token = create_jwt(username, "user")  # no admin :)
            return redirect(url_for("index"))
        return "Invalid credentials"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    if "username" not in session:
        return redirect(url_for("login"))  # must be logged in

    rendered = None
    if request.method == "POST":
        template = request.form.get("template", "")
        rendered = render_template_string(
            template,
            username=session.get("username"),
            config=app.config
        )

    return render_template(
        "profile.html",
        username=session.get("username"),
        rendered=rendered
    )

@app.route("/flag")
def flag_page():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth.split(" ")[1]
    payload = decode_jwt(token)
    if not payload or payload.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    return render_template("flag.html", flag=FLAG)


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)

