from flask import Blueprint, render_template, request, flash, redirect
from flask import current_app as app
from pyotp import TOTP
import os

bp = Blueprint("drop", __name__)

@bp.route("/drop", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        totp = TOTP(app.config["TOTP_SECRET"])
        if "authcode" not in request.form:
            flash("Missing OTP")
            return redirect(request.url)

        if not totp.verify(request.form["authcode"]):
            flash("Incorrect OTP")
            return redirect(request.url)

        if not request.files:
            flash("No files field")
            return redirect(request.url)

        files = (f for f in request.files.getlist("files") if f.filename != "")

        if not files:
            flash("No files specified")
            return redirect(request.url)

        for file in files:
            file.save(os.path.join(app.config["UPLOAD_DIR"], file.filename))

        return redirect("/drop")

    return render_template("drop.html")


