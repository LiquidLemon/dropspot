from flask import Blueprint, render_template, request, flash, redirect
from flask import current_app as app
from pyotp import TOTP
import os

bp = Blueprint("drop", __name__)


@bp.route("/drop", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        totp = TOTP(app.config["TOTP_SECRET"])
        if request.form["authcode"] == "":
            flash("Missing OTP", "error")
            return redirect(request.url)

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

        for file in files:
            file.save(os.path.join(app.config["UPLOAD_DIR"], file.filename))

        flash("Files uploaded correctly!", "success")
        return redirect("/drop")

    return render_template("drop.html")
