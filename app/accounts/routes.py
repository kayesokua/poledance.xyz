from flask import Blueprint, flash, redirect, render_template, url_for, session, request
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from app import db
from app.models.user import User
from .forms import SignInForm, SignUpForm
import pytz
import bcrypt

bp = Blueprint("accounts", __name__, url_prefix="/accounts")
tz = pytz.timezone('UTC')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect(url_for("accounts.sign_in"))

@bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = SignInForm()
    if current_user.is_authenticated:
        return redirect(url_for('accounts.profile'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('accounts.profile'))
        else:
            flash('Invalid email or password')

    return render_template("form.html", form=form, title="Sign In")

@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if current_user.is_authenticated:
        return redirect(url_for("accounts.profile"))

    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        print("validated")
        if user:
            flash('Username or email already exists', 'error')
            return render_template("form.html", form=form, title="Sign Up")
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt).decode('utf-8')

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash('Registration successful', 'success')
        return redirect(url_for('accounts.profile'))

    return render_template("form.html", form=form, title="Sign Up")

@bp.route("/sign-out")
@login_required
def sign_out():
    session.clear()
    logout_user()
    return redirect(url_for('accounts.sign_in'))

@bp.route("/profile", methods=["GET", "POST"], endpoint="profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")

