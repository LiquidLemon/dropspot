from flask import Blueprint, request, render_template, flash, redirect

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["email"] == "":
            flash("Missing email", "error")
            return redirect(request.url)

        if request.form["password"] == "":
            flash("Missing password", "error")
            return redirect(request.url)

        if request.form["confirm-password"] == "":
            flash("Missing password confirm", "error")
            return redirect(request.url)

        password = request.form["password"]
        c_password = request.form["confirm-password"]

        if password != c_password:
            flash("Fields Password and Confirm must be the same", "error")
            return redirect(request.url)

        if len(password) < 8:
            flash("Password must be at least 8 characters long", "error")
            return redirect(request.url)

        flash("registered successfully", "success")
        return redirect("/drop")

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
