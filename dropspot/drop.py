from flask import Blueprint, render_template, request, flash, redirect, session
from flask import current_app as app
from pyotp import TOTP
import os
from dropspot.models import db, User

bp = Blueprint("drop", __name__)


@bp.route("/drop", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]

        if username == "":
            flash("Missing Username", "error")
            return redirect(request.url)

        if request.form["authcode"] == "":
            flash("Missing OTP", "error")
            return redirect(request.url)

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("Given username does not exist", "error")
            return redirect(request.url)

        totp = TOTP(user.otp_secret)

        if not totp.verify(request.form["authcode"]):
            flash("Incorrect OTP", "error")
            return redirect(request.url)

        if not request.files:
            flash("No files field", "error")
            return redirect(request.url)

        files = (f for f in request.files.getlist("files") if f.filename != "")

        if not files:
            flash("No files specified", "error")
            return redirect(request.url)

        path = app.config["UPLOAD_DIR"] + "/" + user.username

        if not os.path.isdir(path):
            os.mkdir(path)

        for file in files:
            file.save(os.path.join(path, file.filename))

        flash("Files uploaded correctly!", "success")
        return redirect("/drop")

    return render_template("drop.html", user_email=session.get("user_email"))
