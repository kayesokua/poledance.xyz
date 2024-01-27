from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
from flask_login import LoginManager, current_user
from flask_moment import Moment

from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from app.extensions.db import db, migrate


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    csrf = CSRFProtect(app)
    bootstrap = Bootstrap(app)
    moment = Moment(app)


    with app.app_context():
        from app.models import User, VideoPost
        db.create_all()
        migrate.init_app(app, db, compare_type=True)
    
    from app.api.routes import bp as api
    from app.accounts.routes import bp as accounts
    from app.diary.routes import bp as diary
    from app.reports.routes import bp as reports
    
    app.register_blueprint(api)
    app.register_blueprint(accounts)
    app.register_blueprint(diary)
    app.register_blueprint(reports)
    
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
        if current_user.is_authenticated:
            return redirect(url_for("diary.all_dance_entries"))

        return render_template("/index.html", title="Cover")

    return app