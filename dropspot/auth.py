from flask import Blueprint, request, render_template, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from dropspot.models import db, User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form["password"]
        c_password = request.form["confirm-password"]
        email = request.form["email"]

        if email == "":
            flash("Missing email", "error")
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

        if User.query.filter_by(email=email).first() is not None:
            flash("User with this email is registered already", "error")
            return redirect(request.url)

        user = User(email=email, password_hash=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        flash("registered successfully", "success")
        return redirect("/drop")

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        email = request.form["email"]

        if email == "":
            flash("Missing email", "error")
            return redirect(request.url)

        if password == "":
            flash("Missing password", "error")
            return redirect(request.url)

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("User with this email is does not exist", "error")
            return redirect(request.url)

        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password", "error")
            return redirect(request.url)

        flash("Logged in successfully")
        return redirect("/drop")

    return render_template("login.html")
