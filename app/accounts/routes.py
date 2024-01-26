from flask import Blueprint, render_template
from .forms import SignUpForm, SignInForm
import pytz

bp = Blueprint("accounts", __name__, url_prefix="/accounts")
tz = pytz.timezone('UTC')

@bp.route("/login", methods=["GET", "POST"])
def index():
    form=SignInForm()
    
    return render_template("form.html", form=form, title="Log In")

@bp.route("/register", methods=["GET", "POST"])
def register():
    form=SignUpForm()
    return render_template("form.html", form=form, title="Register")

