from flask import Blueprint, request, render_template, flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from dropspot.models import db, User
import pyotp

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id") is not None:
        flash("Already logged in", "success")
        return redirect("/drop")

    if request.method == "POST":
        password = request.form["password"]
        c_password = request.form["confirm-password"]
        username = request.form["username"]

        if username == "":
            flash("Missing username", "error")
            return redirect(request.url)

        if password == "":
            flash("Missing password", "error")
            return redirect(request.url)

        if c_password == "":
            flash("Missing password confirm", "error")
            return redirect(request.url)

        if password != c_password:
            flash("Fields Password and Confirm must be the same", "error")
            return redirect(request.url)

        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return redirect(request.url)

        if User.query.filter_by(username=username).first() is not None:
            flash("User with this username is registered already", "error")
            return redirect(request.url)

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            otp_secret=pyotp.random_base32(),
        )

        db.session.add(user)
        db.session.commit()

        flash("registered successfully", "success")
        return redirect("/drop")

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id") is not None:
        flash("Already logged in", "success")
        return redirect("/drop")

    if request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]

        if username == "":
            flash("Missing username", "error")
            return redirect(request.url)

        if password == "":
            flash("Missing password", "error")
            return redirect(request.url)

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("User with this username does not exist", "error")
            return redirect(request.url)

        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password", "error")
            return redirect(request.url)

        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username

        flash("Logged in successfully", "success")
        return redirect("/drop")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/drop")
