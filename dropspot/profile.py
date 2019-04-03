from flask import Blueprint, render_template, session, redirect, flash
from flask import current_app as app
import pyotp
from dropspot.models import db, User

bp = Blueprint("profile", __name__)


@bp.route("/profile")
def profile():
    user_id = session.get("user_id")
    if user_id is None:
        flash("You must be logged in to view profile", "error")
        return redirect("/login")

    user = User.query.get(user_id)
    otp_secret = user.otp_secret

    totp = pyotp.TOTP(otp_secret)
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
        "drop@spot.com", issuer_name="Drop Spot"
    )

    return render_template(
        "profile.html",
        username=session.get("username"),
        otp_uri=otp_uri,
        user=user,
    )
