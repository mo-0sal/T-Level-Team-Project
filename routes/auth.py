from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, flash, render_template, abort
from werkzeug.security import check_password_hash
from database import get_db

auth_bp = Blueprint("auth", __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to access this page", "error")
                return redirect(url_for("auth.login"))
            if session.get("role") not in roles:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect(url_for("auth.login"))

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["full_name"] = user["full_name"]
    session["department"] = user["department"]

    flash(f"Welcome back, {user['full_name']}!", "success")
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
   
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("auth.login"))
