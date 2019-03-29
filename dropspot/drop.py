from flask import Blueprint, render_template, request, flash, redirect
from flask import current_app as app
import os

bp = Blueprint("drop", __name__)

@bp.route("/drop", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.files:
            flash("No files field")
            redirect(request.url)

        files = [f for f in request.files if f.filename != ""]
        if not files:
            flash("No files specified")
            redirect(request.url)

        for file in files:
            file.save(os.path.join(app.config["UPLOAD_DIR"], file.filename))

        return redirect("/")

    return render_template("drop.html")
