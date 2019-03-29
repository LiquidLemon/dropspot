from flask import Blueprint, request, render_template

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
