from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
from flask_login import LoginManager

from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from app.extensions.db import db, migrate


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    csrf = CSRFProtect(app)
    db.init_app(app)
    bootstrap = Bootstrap(app)

    with app.app_context():
        from app.models import User
        db.create_all()
        migrate.init_app(app, db, compare_type=True)
    
    from app.accounts.routes import bp as accounts
    app.register_blueprint(accounts)
    
    app.add_url_rule("/sign-in", endpoint='accounts.sign_in')
    app.add_url_rule("/sign-up", endpoint='accounts.sign_up')
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.sign_in'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    @app.route("/")
    def index():
        return render_template("/index.html", title="Cover")

    return app