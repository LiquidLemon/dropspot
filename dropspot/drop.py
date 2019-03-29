from flask import Blueprint, render_template

bp = Blueprint('drop', __name__)

@bp.route('/')
def index():
    return render_template('drop.html')
